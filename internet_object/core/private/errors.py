

INVALID_DATATYPE          = 'invalid-datatype'
INVALID_KEY               = 'invalid-key'
INVALID_OPERATION         = 'invalid-operation'

INVALID_POSITIONAL_VALUE  = 'invalid-poistional-value'

MORE_THAN_ONE_VALUE       = 'more-than-one-value'


VALUE_REQUIRED            = 'value-required'
OBJECT_REQUIRED           = 'object-required'



class ValidationError(Exception):
  def __init__(self, message, errors=None):

    # Call the base class constructor with the parameters it needs
    super(ValidationError, self).__init__(message)

    # Now for your custom code...
    self.errors = errors
