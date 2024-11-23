from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()
db = SessionLocal()

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Person(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    isMale: bool
    
    
@app.get('/', response_model=list[Person], status_code=status.HTTP_200_OK)
def getAllPersons():
    getAllPerson = db.query(models.Person).all()
    return getAllPerson


@app.post('/addperson', response_model=Person, status_code=status.HTTP_200_OK)
def add_Person(person: Person):
    newPerson = models.Person(
        id= person.id,
        firstname= person.firstname,
        lastname= person.lastname,
        isMale= person.isMale
    )
    
    find_person = db.query(models.Person).filter(models.Person.id == person.id).first()
    
    if find_person is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id already exists!")
    
    db.add(newPerson)
    db.commit()
    db.refresh(newPerson)
    
    return newPerson


@app.put('/update/{person_id}', response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def updatePerson(person_id: int, person: Person):
    
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    
    if find_person is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id does not exists!")
    
    find_person.firstname = person.firstname
    find_person.lastname = person.lastname
    find_person.isMale = person.isMale
    db.commit()
    
    return find_person


@app.delete('/delete/{person_id}', response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def deletePerson(person_id: int):
    
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    
    if find_person is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id does not exists!")
    
    db.delete(find_person)
    db.commit()
    
    return find_person


@app.get('/get/{person_id}', response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def getSinglePerson(person_id: int):
    
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    
    if find_person is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id does not exists!")
    
    return find_person