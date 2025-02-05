class RBApplication:
    def __init__(self, application_id: int | None = None,
                 subscriber_number: int | None = None,
                 user_id_created_application: int | None = None,
                 application_status: int | None = None):
        self.application_id = application_id
        self.subscriber_number = subscriber_number
        self.user_id_created_application = user_id_created_application
        self.application_status = application_status

        
    def to_dict(self) -> dict:
        data = {'application_id': self.application_id, 'subscriber_number': self.subscriber_number, 'user_id_created_application': self.user_id_created_application,
                'application_status': self.application_status}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data