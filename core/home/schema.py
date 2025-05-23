from graphene_django.types import DjangoObjectType, ObjectType
from .models import Person, Car
import graphene



class PersonType(DjangoObjectType):
    class Meta:
        model = Person


class CarType(DjangoObjectType):
    class Meta:
        model = Car


class HomeQuery(ObjectType):
    persons = graphene.List(PersonType)
    cars = graphene.List(CarType)
    person = graphene.Field(PersonType, id=graphene.Int(), name=graphene.String())
    car = graphene.Field(CarType, id=graphene.Int(), name=graphene.String())


    def resolve_persons(parent, info, **kwargs):
        return Person.objects.all()
    

    def resolve_cars(parent, info, **kwargs):
        return Car.objects.all()


    def resolve_person(parent, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        if id and name is not None:
            return Person.objects.get(id=id, name=name)
        if id is not None:
            return Person.objects.get(id=id)
        if name is not None:
            return Person.objects.get(name=name)
        return None

    def resolve_car(parent, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        if id and name is not None:
            return Car.objects.get(id=id, name=name)
        if id is not None:
            return Car.objects.get(id=id)
        if name is not None:
            return Car.objects.get(name=name)
        return None


class PersonInput(graphene.InputObjectType):
    name = graphene.String()
    age = graphene.Int()
    
class CarInput(graphene.InputObjectType):
    persons_id = graphene.List(graphene.ID)
    name = graphene.String()
    year = graphene.Int()
    

class CreatePerson(graphene.Mutation):
    class Arguments:
        input = PersonInput(required=True)

    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    def mutate(parent, info, input=None):
        person_instance = Person.objects.create(name=input.name, age=input.age)
        ok = True
        return CreatePerson(person=person_instance, ok=ok)



class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PersonInput()


    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=None)

    def mutate(parent, info, id, input=None):
        person_instance = Person.objects.get(id=id)
        person_instance.name = input.name if input.name is not None else person_instance.name
        person_instance.age = input.age if input.age is not None else person_instance.age
        person_instance.save()

        ok=True
        return UpdatePerson(person=person_instance, ok=ok)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)


    def mutate(parent, info, id):
        person_instance = Person.objects.get(id=id)
        person_instance.delete()
        ok = True
        return DeletePerson(person=person_instance, ok=ok)


class CreateCar(graphene.Mutation):
    class Arguments:
        input = CarInput()


    car = graphene.Field(CarType)
    ok = graphene.Boolean(default_value=False)

    def mutate(parent, info, input=None):
        persons_list = []
        for person_id in input.persons_id:
            person_instance = Person.objects.get(id=person_id)
            persons_list.append(person_instance)


        car_instance = Car.objects.create(name=input.name, year=input.year)
        car_instance.person.set(persons_list)
        ok = True
        return CreateCar(car=car_instance, ok=ok)

class Mutate(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()
    create_car = CreateCar.Field()
