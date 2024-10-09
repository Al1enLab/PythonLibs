'''
Classes de gestion de variables (de configuration, principalement)

Une variable a les propriétés suivantes :
- default : sa valeur par défaut
- type : le type souhaité de la variable
- mandatory : est-elle obligatoire ou pas
- strict : le type de la variable doit-il être strictement respecté ou pas
- retrieved : flag interne : valeur retournée par .value() oui / non

Enfin, la méthode .value() décorée par @Value, qui retourne la valeur de la variable.

Par exemple :
V = EnvironmentVariable('HOME')
print(V.value)
affichera la valeur de la variable d'environnement HOME, ou None si elle n'est pas définie.
'''
from dataclasses import dataclass, field
import os
import configparser
import argparse
from typing import Mapping, Any

class Value:
    '''Décorateur de la fonction de retour de la valeur des classes Variable
    La méthode .value() est utilisée comme une propriété.
    Procède aux différents tests sur le retour à faire :
    - Si la valeur peut être récupérée
    - Si elle est obligatoire
    - Si elle doit être typée
    - Si tout ça est strict ou pas
    '''
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        try:
            value = self.func(instance)
            setattr(instance, 'retrieved', True)
        except Exception as E:
            if instance.mandatory:
                raise Exception(E)
            else:
                return instance.default
        if instance.type is not None:
            try:
                return instance.type(value)
            except Exception as E:
                if instance.strict:
                    raise Exception(E)
                else:
                    return value
        return value

@dataclass(kw_only=True)
class BaseVariable:
    # Valeur par défaut si .value() échoue
    default: Any = None
    # Type à affecter à la vairable de sortie
    type: Any = None
    # Raise si .value() échoue
    mandatory: bool = False
    # Raise si le typage échoue
    strict: bool = False
    # Flag : .value() a retourné une valeur oui/non
    retrieved = False

def PreferredVariable(*variables: list[BaseVariable]) -> Any:
    '''Retourne la première valeur trouvée dans les objets Variables passés an paramètre,
    ou la première valeur par défaut si aucune valeur n'est trouvée.'''
    for variable in variables:
        value = variable.value
        if not hasattr(variable,'retrieved') or (hasattr(variable, 'retrieved') and variable.retrieved):
            return value
    return variables[0].value

@dataclass
class DefaultValue:
    value: Any

'''
Toutes les classes suivantes contiennent:
- les paramètres typés
- une méthode .value() décorée par @Value qui retourne la valeur en fonction des paramères
'''
@dataclass
class EnvironmentVariable(BaseVariable):
    variable: str
    environment: Mapping = field(default_factory=lambda: os.environ)

    @Value
    def value(self):
        return self.environment[self.variable]

@dataclass
class ConfigFileVariable(BaseVariable):
    config: configparser
    section: str
    variable: str

    @Value
    def value(self):
        return self.config[self.section][self.variable]

@dataclass
class CommandArgument(BaseVariable):
    parsedargs: argparse
    variable: str

    @Value
    def value(self):
        return getattr(self.parsedargs, self.variable)
