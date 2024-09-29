
class Predictor:
    def __init__(self, foo):
        self.foo = foo

    def predict(self, strings):
        result_strings = []
        result_numbers = []
        for string in strings:
            # Применение функции foo к строке и сохранение результата в список
            result_string, *result_number = self.foo(string)
            result_strings.append(result_string)
            result_numbers.append(result_number)
        
        # Возвращение нового массива строк и пары чисел
        return result_strings, result_numbers
    
    def proceed(self, input):
        pass