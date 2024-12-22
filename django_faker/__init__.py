"""

Django-faker uses python-faker to generate test data for Django models and templates.

"""



__version__ = '0.2.1'

class Faker(object):
    instance = None
    populators = {}
    generators = {}

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Faker, cls).__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        pass

    @staticmethod
    def getCodename(locale=None, providers=None):
        """
        codename = locale[-Provider]*
        """
        from django.conf import settings
        # language
        locale = locale or getattr(settings,'FAKER_LOCALE', getattr(settings,'LANGUAGE_CODE', None))
        # providers
        providers = providers or getattr(settings,'FAKER_PROVIDERS', None)

        codename = locale or 'default'

        if providers:
            codename += "-" + "-".join(sorted(providers))

        return codename

    @classmethod
    def getGenerator(cls, locale=None, providers=None, codename=None):
        """
        use a codename to cache generators
        """
        codename = codename or cls.getCodename(locale, providers)

        if codename not in cls.generators:
            from faker import Faker as FakerGenerator
            generator = FakerGenerator(locale=locale)
            if providers:
                for provider in providers:
                    generator.add_provider(provider)
            cls.generators[codename] = generator
            FakerGenerator.seed()

        return cls.generators[codename]

    @classmethod
    def getPopulator(cls, locale=None, providers=None):
        """
        uses:
            from django_faker import Faker
            pop = Faker.getPopulator()
            
            from myapp import models
            pop.addEntity(models.MyModel, 10)
            pop.addEntity(models.MyOtherModel, 10)
            pop.execute()
        """
        codename = cls.getCodename(locale, providers)

        if codename not in cls.populators:
            generator = cls.generators.get(codename, None) or cls.getGenerator(codename=codename)
            from django_faker import populator
            cls.populators[codename] = populator.Populator(generator)

        return cls.populators[codename]