import enum


class StrEnum(str, enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def to_enum_string_list(clz):
        attrs = vars(clz)
        candidate_enum_string = list()
        for k, v in attrs.items():
            if not callable(k) and not k.startswith('_'):
                candidate_enum_string.append(v.name)
        return f'Enum : {str(candidate_enum_string)}'
