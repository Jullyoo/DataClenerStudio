from datetime import datetime


class TransformationHistory:

    def __init__(self):

        self.history = []

    def add_action(
        self,
        action_name,
        before_shape,
        after_shape
    ):

        self.history.append({

            'action': action_name,

            'before_shape': before_shape,

            'after_shape': after_shape,

            'timestamp': datetime.now().isoformat()
        })

    def get_history(self):

        return self.history

    def clear_history(self):

        self.history = []