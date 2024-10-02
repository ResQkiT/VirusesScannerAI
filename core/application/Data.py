class Data:
    
    def __init__(self, list : list, is_expired = False) -> None:
        if is_expired:
            self.list_ = []
            self.expire = True

        self.list_ = list
        self.expired = is_expired

    def is_expired(self) -> bool:
        return self.expired
    
    def get_data(self) -> list:
        if self.expired:
            raise RuntimeError("data is not valid")
        else:
            return self.list_
    
    def expire(self):
        self.expired = True
