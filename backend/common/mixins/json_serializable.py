from sqlalchemy.inspection import inspect
from decimal import Decimal
from datetime import datetime, date
import json


class JSONSerializable:
    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        try:
            mapper = inspect(self)
            attrs = mapper.mapper.column_attrs
        except Exception:
            attrs = None

        if attrs:
            data = {
                c.key: getattr(self, c.key)
                for c in attrs
                if c.key not in exclude
            }
        else:
            data = {
                k: v
                for k, v in self.__dict__.items()
                if not k.startswith("_") and k not in exclude
            }

        return self._normalize(data)

    def _normalize(self, data):
        if isinstance(data, dict):
            return {k: self._normalize(v) for k, v in data.items()}

        if isinstance(data, list):
            return [self._normalize(v) for v in data]

        if isinstance(data, Decimal):
            return float(data)

        if isinstance(data, (datetime, date)):
            return data.isoformat()

        return data

    def to_content_dict(self):
        """Return business content suitable for LLM context, without persistence identifiers."""
        data = self.to_dict()
        return {
            key: value
            for key, value in data.items()
            if key != "id" and not key.endswith("_id")
        }

