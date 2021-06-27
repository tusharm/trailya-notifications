class DatasetErrors:
    def __init__(self):
        self._errors = []

    def try_operation(self, func, returned_on_error='', msg=''):
        try:
            return func()
        except Exception as e:
            self._add(msg, e)
            return returned_on_error

    def _add(self, msg: str, e: Exception):
        self._errors.append({
            'message': msg,
            'exception': getattr(e, 'message', repr(e))
        })

    def get(self) -> []:
        return self._errors
