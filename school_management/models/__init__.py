# Import models in dependency order
from . import teacher          # Teacher model - base model with no dependencies
from . import class_room       # Class model - depends on teacher
from . import student         # Student model - depends on class and teacher  
from . import account_extension         # Student model - depends on class and teacher  
from . import student_invoice_scheduler