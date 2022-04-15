import pytest
from itertree import *

__argument__ = 'FAKE'


class ObservableiDataModel(Data.iTDataModel):

    def __init__(self, value=Data.__NOVALUE__, state=True, text='ok'):
        self.state = state
        self.text = text
        super().__init__(value)

    def _validator(self, value):
        return self.state, self.text

@pytest.fixture
def setup_no_argument():
    object_under_test = ObservableiDataModel()
    yield object_under_test


@pytest.fixture
def setup_fake_argument():
    object_under_test = ObservableiDataModel(value=__argument__)
    yield object_under_test


class TestiTDataModelInit:

    def test_init_no_arguments(self, setup_no_argument):
        assert setup_no_argument.value is None and \
               setup_no_argument._formatter_cache is None

    def test_init_value_argument(self, setup_fake_argument):
        assert setup_fake_argument.value == __argument__ and \
               setup_fake_argument._formatter_cache is None

    def test_init_value_invalid_argument(self):
        with pytest.raises(ValueError):
            class_under_test = ObservableiDataModel(value=__argument__, state=False)


class TestiTDataModelProperties:

    def test_is_empty_property(self, setup_no_argument, setup_fake_argument):
        assert setup_no_argument.is_empty is True and setup_fake_argument.is_empty is False

    def test_value_property(self, setup_no_argument, setup_fake_argument):
        assert setup_no_argument.value is None and setup_fake_argument.value is __argument__


class TestiTDataModelMethods:
    state_data = [(True, __argument__),
                  (False, None)]

    def test_clear_value(self, setup_fake_argument):
        assert setup_fake_argument.clear_value() is __argument__ and \
               setup_fake_argument.value is None

    def test_clear_value_empty_value(self, setup_no_argument):
        assert setup_no_argument.clear_value() is None and \
               setup_no_argument.value is None

    def test__validator(self, setup_fake_argument):
        assert setup_fake_argument._validator(None) == (True, 'ok')

    def test_emptyformatter_empty(self, setup_no_argument):
        assert setup_no_argument._formatter() is 'None'

    def test_emptyformatter_not_empty(self, setup_fake_argument):
        assert setup_fake_argument._formatter() is 'FAKE'

    def test_formatter_empty(self, setup_no_argument):
        assert setup_no_argument._formatter('Kraftfahrzeug-Haftpflichtversicherung') is \
               'Kraftfahrzeug-Haftpflichtversicherung'

    def test_formatter_empty_not_empty(self, setup_fake_argument):
        assert setup_fake_argument._formatter('Massenkommunikationsdienstleistungsunternehmen') is \
               'Massenkommunikationsdienstleistungsunternehmen'

    @pytest.mark.parametrize("state, expected", state_data)
    def test_set_state(self, state, expected):
        object_under_test = ObservableiDataModel(state=state)
        if state is False:
            with pytest.raises(TypeError):
                object_under_test.set(expected)
        else:
            object_under_test.set(expected)
            assert object_under_test.value == __argument__

    @pytest.mark.parametrize("state, expected", state_data)
    def test_check(self, state, expected):
        object_under_test = ObservableiDataModel(state=state)
        if state is False:
            assert object_under_test.check(3) == (False, 'ok')
        else:
            assert object_under_test.check(5) == (True, 'ok')

    def test_contains(self, setup_fake_argument):
       assert __argument__ in setup_fake_argument

    def test_not_contains(self, setup_fake_argument):
       assert None not in setup_fake_argument

    def test_contains_empty(self, setup_no_argument):
       assert Data.__NOVALUE__ in setup_no_argument

    def test_contains_none(self):
        object_under_test = Data.iTDataModel(value=None)
        assert None in object_under_test

    def test_not_contains_empty(self, setup_no_argument):
       assert __argument__ not in setup_no_argument

    def test_format_empty_no_format_spec(self, setup_no_argument):
        assert format(setup_no_argument) is 'None'

    def test_no_format_spec(self, setup_fake_argument):
        assert format(setup_fake_argument) is __argument__

    def test_format_spec(self, setup_fake_argument):
        # Failing here.
        assert format(Data.iTDataModel(10), 'x') is 'a'

    def test_repr_empty(self, setup_no_argument):
        assert str(setup_no_argument) == 'iTreeDataModel()'

    def test_repr_not_empty(self, setup_fake_argument):
        assert str(setup_fake_argument) == 'iTreeDataModel(value= %s)' %__argument__

__raw_data__ = 'raw_data'
@pytest.fixture
def iTData_setup():
    fake_model = ObservableiDataModel()
    object_under_test = Data.iTData({__raw_data__: fake_model})
    yield object_under_test

@pytest.fixture
def iTData_setup_setup_no_argument():
    object_under_test = Data.iTData()
    yield object_under_test

@pytest.fixture
def iTData_as_dict():
    object_under_test = Data.iTData({'one': 1, 'two': 2, 'three': 3})
    yield object_under_test



class TestiTDataInit:

    def test_init_no_arguments(self, iTData_setup_setup_no_argument):
        assert not bool(iTData_setup_setup_no_argument)

    def test_init_value_argument(self, iTData_setup):
        assert __raw_data__ in iTData_setup and bool(iTData_setup)

    def test_init_type_error(self):
        object_under_test = Data.iTData((1,2,3))
        assert bool(object_under_test) and \
               Data.__NOKEY__ in object_under_test.keys() and \
               object_under_test[Data.__NOKEY__] == (1,2,3)

    def test_init_value_error(self):
        object_under_test = Data.iTData({'Hello'})
        assert bool(object_under_test) and \
               Data.__NOKEY__ in object_under_test.keys() and \
               object_under_test[Data.__NOKEY__] == {'Hello'}


class TestiTDataProperties:
    pass


class TestiTDataMethods:
    pass


class TestiTDataDictionaryConsistency:

    def test_init_key_with_kwargs(self):
        object_under_test = Data.iTData(one = 1, two = 2, three = 3)
        assert bool(object_under_test) and \
               object_under_test['one'] == 1 and \
               object_under_test['two'] == 2 and \
               object_under_test['three'] == 3

    def test_init_with_mapping(self):
        object_under_test = Data.iTData({'one': 1, 'two': 2, 'three': 3})
        assert bool(object_under_test) and \
               object_under_test['one'] == 1 and \
               object_under_test['two'] == 2 and \
               object_under_test['three'] == 3

    def test_init_with_iterable(self):
        object_under_test = Data.iTData(zip(['one', 'two', 'three'], [1, 2, 3]))
        assert bool(object_under_test) and \
               object_under_test['one'] == 1 and \
               object_under_test['two'] == 2 and \
               object_under_test['three'] == 3

    def test_init_with_iterable_2(self):
        object_under_test = Data.iTData([('two', 2), ('one', 1), ('three', 3)])
        assert bool(object_under_test) and \
               object_under_test['one'] == 1 and \
               object_under_test['two'] == 2 and \
               object_under_test['three'] == 3

    def test_init_with_generator(self):
        def dict_generator():
                var = (('one', 1),('two', 2),('three', 3))
                for elem in var:
                    yield elem

        object_under_test = Data.iTData(dict_generator())
        assert bool(object_under_test) and \
               object_under_test['one'] == 1 and \
               object_under_test['two'] == 2 and \
               object_under_test['three'] == 3

    def test_init_with_dict_comprehension(self):
        object_under_test = Data.iTData({x: x ** 2 for x in (1, 2, 3)})
        assert bool(object_under_test) and \
               object_under_test[1] == 1 and \
               object_under_test[2] == 4 and \
               object_under_test[3] == 9

    def test_init_with_mapping_and_keyword(self):
        object_under_test = Data.iTData({'one': 1, 'three': 3}, two=2)
        assert bool(object_under_test) and \
               object_under_test['one'] == 1 and \
               object_under_test['two'] == 2 and \
               object_under_test['three'] == 3

    def test_method_clear(self, iTData_as_dict):
        empty_dict = iTData_as_dict.clear()
        assert not bool(iTData_as_dict)

    def test_method___contains__(self, iTData_as_dict):
        assert 'two' in iTData_as_dict

    def test_method_copy(self, iTData_as_dict):
        copied_dict = iTData_as_dict.copy()
        assert copied_dict == iTData_as_dict

    def test_method___del_item__(self, iTData_as_dict):
        del iTData_as_dict['two']
        assert 'two' not in iTData_as_dict

    def test_method_fromkeys(self):
        object_under_test = Data.iTData.fromkeys(['one', 'two', 'three'])
        values = set(object_under_test.values())
        assert (len(object_under_test) == 3) and \
               (values == {None})

    def test_method_fromkeys_with_values(self):
        object_under_test = Data.iTData.fromkeys(['one', 'two', 'three'], (5))
        values = set(object_under_test.values())
        assert (len(object_under_test) == 3) and \
               (values == {5})

    def test_method_get(self, iTData_as_dict):
        assert iTData_as_dict.get('two', 3) is 2 and \
               iTData_as_dict.get('ten', 3) is 3

    def test_method___get_item__exception(self, iTData_as_dict):
        with pytest.raises(KeyError):
            iTData_as_dict.__getitem__('ten')

    def test_method___get_item__(self, iTData_as_dict):
        assert iTData_as_dict.__getitem__('two') is 2

    def test_method_items(self, iTData_as_dict):
        view = iTData_as_dict.items()
        assert Data.iTData(view) == iTData_as_dict

    def test_method___iter__(self, iTData_as_dict):
        iterator = iter(iTData_as_dict)
        assert list(iterator) == list(iTData_as_dict.keys())

    def test_method_keys(self, iTData_as_dict):
        assert set(iTData_as_dict.keys()) == {'one', 'two', 'three'}

    def test_method_len(self, iTData_as_dict):
        assert len(iTData_as_dict) == 3

    def test_method_pop(self, iTData_as_dict):
        popped_value = iTData_as_dict.pop('one')
        assert popped_value == 1 and \
               len(iTData_as_dict) == 2 and \
               'one' not in iTData_as_dict

    def test_method_pop_missing(self, iTData_as_dict):
        popped_value = iTData_as_dict.pop('ten', 'MISSING VALUE')
        assert popped_value == 'MISSING VALUE' and \
               len(iTData_as_dict) == 3

    def test_method_pop_missing_2(self, iTData_as_dict):
        with pytest.raises(KeyError):
            popped_value = iTData_as_dict.pop('ten')

    def test_method_pop_item(self, iTData_as_dict):
        iTData_as_dict.popitem()
        assert len(iTData_as_dict) == 2

    def test_method_setdefault(self, iTData_as_dict):
        iTData_as_dict.setdefault('ten', []).append(10)
        assert iTData_as_dict['ten'] == [10]

    def test_method_setdefault(self, iTData_as_dict):
        iTData_as_dict.setdefault('two', []).__repr__()
        assert iTData_as_dict.setdefault('two', []).__repr__() == '2'

    def test_method___setitem__(self, iTData_as_dict):
        iTData_as_dict.__setitem__('ten', 10)
        assert iTData_as_dict['ten'] == 10

    def test_method___setitem__existing(self, iTData_as_dict):
        iTData_as_dict.__setitem__('two', 10)
        assert iTData_as_dict['two'] == 10

    def test_method_update_with_iterable(self, iTData_as_dict):
        iTData_as_dict.update(zip(['four', 'five', 'six'], [4, 5, 6]))
        assert len(iTData_as_dict) == 6 and \
               iTData_as_dict['four'] == 4 and \
               iTData_as_dict['five'] == 5 and \
               iTData_as_dict['six'] == 6

    def test_method_update_with_mapping(self, iTData_as_dict):
        iTData_as_dict.update({'four':4, 'five':5, 'six':6})
        assert len(iTData_as_dict) == 6 and \
               iTData_as_dict['four'] == 4 and \
               iTData_as_dict['five'] == 5 and \
               iTData_as_dict['six'] == 6

    def test_method_update_with_kwargs(self, iTData_as_dict):
        iTData_as_dict.update(four=4, five=5, six=6)
        assert len(iTData_as_dict) == 6 and \
               iTData_as_dict['four'] == 4 and \
               iTData_as_dict['five'] == 5 and \
               iTData_as_dict['six'] == 6

    def test_method_update_with_iterable_and_kwargs(self, iTData_as_dict):
        iTData_as_dict.update(zip(['seven', 'eight', 'nine'], [7, 8, 9]), four=4, five=5, six=6)

        assert len(iTData_as_dict) == 9 and \
               iTData_as_dict['four'] == 4 and \
               iTData_as_dict['five'] == 5 and \
               iTData_as_dict['six'] == 6 and \
               iTData_as_dict['seven'] == 7 and \
               iTData_as_dict['eight'] == 8 and \
               iTData_as_dict['nine'] == 9

    def test_method_update_with_mapping_and_kwargs(self, iTData_as_dict):
        iTData_as_dict.update()
        iTData_as_dict.update({'seven':7, 'eight':8, 'nine':9}, four=4, five=5, six=6)

        assert len(iTData_as_dict) == 9 and \
               iTData_as_dict['four'] == 4 and \
               iTData_as_dict['five'] == 5 and \
               iTData_as_dict['six'] == 6 and \
               iTData_as_dict['seven'] == 7 and \
               iTData_as_dict['eight'] == 8 and \
               iTData_as_dict['nine'] == 9

    def test_method_values(self, iTData_as_dict):
        assert set(iTData_as_dict.values()) == {1, 2, 3}
