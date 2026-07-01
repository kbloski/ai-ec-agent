from sqlalchemy.inspection import inspect
import json

class JSONSerializable:
    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        # 🔥 sprawdź czy obiekt jest SQLAlchemy mapped
        try:
            mapper = inspect(self)
        except Exception:
            # fallback dla zwykłych obiektów
            return {
                k: v
                for k, v in self.__dict__.items()
                if not k.startswith("_") and k not in exclude
            }

        return {
            c.key: getattr(self, c.key)
            for c in mapper.mapper.column_attrs
            if c.key not in exclude
        }

    def to_json(self):
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)