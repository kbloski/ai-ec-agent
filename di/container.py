class Container:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        # init ONLY ONCE
        # self._user_repo = InMemoryUserRepository()

        self._registry = {
            # CreateUserService: self._new_user_service,
        }

    def get(self, service_class):
        try:
            return self._registry[service_class]()
        except KeyError:
            raise ValueError(f"Unknown service: {service_class}")