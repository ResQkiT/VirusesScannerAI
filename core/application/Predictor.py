
class Predictor:
    def __init__(self, foo):
        self.foo = foo

    def single_predict(self, single_string : str) -> tuple:
        result_numbers = ()
        result_numbers = self.foo(single_string)
        return result_numbers
        
    def predict_for_each(self, strings : list) -> map:
        result_map = {}
        for string in strings:
            # Применение функции foo к строке и сохранение результата в список
            result_map[string] = self.foo(string)
        
        # Возвращение нового массива строк и пары чисел
        return result_map
    
    def proceed(self, input):
        pass