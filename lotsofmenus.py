from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Company, MenuCars, User

engine = create_engine('sqlite:///companymenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/\
             2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Menu for Company Toyota
company1 = Company(user_id=1, name="Toyota")
session.add(company1)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Yaris",
                     description="The Yaris is a sedan and wheel-drive type.",
                     price="45,900 SR", company=company1)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Rush",
                     description="Toyota Rush is a multi-use sports car.",
                     price="59,300 SR", company=company1)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="Corolla",
                     description="Toyota Corolla is a sedan-type sedan.",
                     price="60,000 SR", company=company1)
session.add(MenuCars3)
session.commit()

MenuCars4 = MenuCars(user_id=1, name="Camry",
                     description="The Camry LE Standard 2019 is sedan-type.",
                     price="83,000 SR", company=company1)
session.add(MenuCars4)
session.commit()

MenuCars5 = MenuCars(user_id=1, name="Avalon",
                     description="Toyota Avalon 2019 is a sedan-type sedan.",
                     price="116,400 SR", company=company1)
session.add(MenuCars5)
session.commit()


# Menu for Company Mercedes
company2 = Company(user_id=1, name="Mercedes")
session.add(company2)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Mercedes",
                     description="Mercedes Benz is a class-hatchback car.",
                     price="145,000 SR", company=company2)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name=" Mercedes CLA",
                     description=" Mercedes-Benz CLA 2018 is a sedan.",
                     price="168,000 SR", company=company2)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="Mercedes GLA",
                     description="Mercedes-Benz GLA 2018 is a sports car.",
                     price="171,000 SR", company=company2)
session.add(MenuCars3)
session.commit()

MenuCars4 = MenuCars(user_id=1, name="Mercedes C",
                     description="The Mercedes-Benz C 2018 is sedan.",
                     price="193,000 SR", company=company2)
session.add(MenuCars4)
session.commit()

MenuCars5 = MenuCars(user_id=1, name="Mercedes GLC",
                     description="The Mercedes-Benz GLC  2018 is a class.",
                     price="250,000 SR", company=company2)
session.add(MenuCars5)
session.commit()


# Menu for Company Nissan
company3 = Company(user_id=1, name="Nissan")
session.add(company3)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Nissan Sunny",
                     description="Nissan Sunny 2018 is a sedan-type sedan.",
                     price="46,300 SR", company=company3)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Nissan S",
                     description="The Nissan S-2018 is a sedan-type sedan.",
                     price="76,400 SR", company=company3)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="Nissan Maxima S",
                     description="The Nissan Maxima S 2018 is a sedan-type.",
                     price="110,200 SR", company=company3)
session.add(MenuCars3)
session.commit()

MenuCars4 = MenuCars(user_id=1, name="Nissan X-Trail",
                     description="The Nissan X-Trail 2018 is a sports car.",
                     price="77,000 SR", company=company3)
session.add(MenuCars4)
session.commit()

MenuCars5 = MenuCars(user_id=1, name="Nissan Pathfinder",
                     description="The Nissan Pathfinder 2018 is sports car.",
                     price="110,600 SR", company=company3)
session.add(MenuCars5)
session.commit()


# Menu for Company BMW
company4 = Company(user_id=1, name="BMW")
session.add(company4)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="BMW Business",
                     description="The BMW Business 2018 is a sports car.",
                     price="275,000 SR", company=company4)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="BMW Premium",
                     description="The BMW X5 Premium 2018 is a sports car.",
                     price="310,000 SR", company=company4)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="BMW Sport",
                     description="The BMW X5 Sport 2018 is a sports car.",
                     price="410,000 SR", company=company4)
session.add(MenuCars3)
session.commit()


# Menu for Company Dodge
company5 = Company(user_id=1, name="Dodge")
session.add(company5)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Dodge Challenger SXT",
                     description="The Dodge Challenger is a sports-class car",
                     price="124,999 SR", company=company5)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Dodge Challenger SXT Plus",
                     description="The Dodge Challenger Plus 2018 is a sports",
                     price="146,999 SR", company=company5)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="Dodge Challenger R / T",
                     description="The Dodge Challenger R / T is sports-class",
                     price="169,999 SR", company=company5)
session.add(MenuCars3)
session.commit()


# Menu for Company Range Rover
company6 = Company(user_id=1, name="Range Rover")
session.add(company6)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Range Rover Standard",
                     description="The Range Rover Standard is a sports car.",
                     price="462,000 SR", company=company6)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Range Rover Sport",
                     description="Range Rover Sport 2018 is a sports car.",
                     price="430,000 SR", company=company6)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="Range Rover Sport SE",
                     description="The Range Rover SE 2018 is a sports car.",
                     price="381,000 SR", company=company6)
session.add(MenuCars3)
session.commit()


# Menu for Company Porsche
company7 = Company(user_id=1, name="Porsche")
session.add(company7)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Porsche Makan",
                     description="The Porsche Makan BASE 2018 is sports car",
                     price="203,100 SR", company=company7)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Porsche Boxster",
                     description="The Porsche Boxster BASE 2018 is a class.",
                     price="244,500 SR", company=company7)
session.add(MenuCars2)
session.commit()

MenuCars3 = MenuCars(user_id=1, name="Porsche Cayenne",
                     description="The Porsche Cayenne BASE 2018 is a sports",
                     price="231,700 SR", company=company7)
session.add(MenuCars3)
session.commit()


# Menu for Company Chevrolet
company8 = Company(user_id=1, name="Chevrolet")
session.add(company8)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Chevrolet",
                     description="The Chevrolet Cruze LS 2017 is a sedan.",
                     price="52,000 SR", company=company8)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Chevrolet Impala",
                     description="The Chevrolet Impala LS 2018 is a sedan.",
                     price="103,000 SR", company=company8)
session.add(MenuCars2)
session.commit()


# Menu for Company Infiniti
company9 = Company(user_id=1, name="Infiniti")
session.add(company9)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Infiniti Excellence",
                     description="Infiniti Q70 Excellence 3.7 2016 is sedan.",
                     price="175,000 SR", company=company9)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Infiniti Q70 Luxury",
                     description="Infiniti Q70 Luxury 2016 is a sedan.",
                     price="196,000 SR", company=company9)
session.add(MenuCars2)
session.commit()


# Menu for Company GMC
company10 = Company(user_id=1, name="GMC")
session.add(company10)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="GMC Yukon SLE",
                     description="The GMC Yukon SLE 2019 is a sports car.",
                     price="188,000 SR", company=company10)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="GMC Yukon SLE 4 in 4",
                     description="GMC Yukon SLE 4 in 4 2019 is a sports car.",
                     price="200,700 SR", company=company10)
session.add(MenuCars2)
session.commit()


# Menu for Company Ford
company11 = Company(user_id=1, name="Ford")
session.add(company11)
session.commit()

MenuCars1 = MenuCars(user_id=1, name="Ford Taurus SE",
                     description="Ford Taurus SE The Eco-Post 2018 sedan.",
                     price="111,300 SR", company=company11)
session.add(MenuCars1)
session.commit()

MenuCars2 = MenuCars(user_id=1, name="Ford Taurus SE",
                     description="The Ford Taurus SE 2018 is a sedan.",
                     price="119,000 SR", company=company11)
session.add(MenuCars2)
session.commit()


print "added menu cars!"
