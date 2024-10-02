import joblib
import pandas as pd
import numpy as np
import math
import catboost
from rdkit import Chem, DataStructs
from rdkit.Chem import Descriptors, AllChem
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA

class Predictor:
    def __init__(self):
        self.model_v = joblib.load('..\\models\\virus2.joblib')
        self.model_vero = joblib.load('..\\models\\monkey_cc50.joblib')
        
    
    def smiles_to_dataframe(self, smiles_list):
        df =  pd.DataFrame({'Smiles': smiles_list})
        return df
    
    '''meta functions'''
    def rdkit_fp(self, smiles_column: pd.Series, radius=3, nBits=2048, useChirality=False):
        # morganFP_rdkit
        def desc_gen(mol):
            mol = Chem.MolFromSmiles(mol)
            bit_vec = np.zeros((1,), np.int16)
            DataStructs.ConvertToNumpyArray(
                AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=nBits, useChirality=useChirality), bit_vec)
            return bit_vec

        return pd.DataFrame.from_records(smiles_column.apply(func=desc_gen), columns=[f'bit_id_{i}' for i in range(nBits)])


    def rdkit_2d(self,smiles_column: pd.Series):
        # 2d_rdkit
        descriptors = {i[0]: i[1] for i in Descriptors._descList}
        return pd.DataFrame({k: f(Chem.MolFromSmiles(m)) for k, f in descriptors.items()} for m in smiles_column)
    
    async def proceed_for_vero(self, input : list):
  
        removed_columns = ['feature_2050',
                            'feature_2056',
                            'feature_2057',
                            'feature_2058',
                            'feature_2061',
                            'feature_2062',
                            'feature_2065',
                            'feature_2077',
                            'feature_2078',
                            'feature_2079',
                            'feature_2080',
                            'feature_2081',
                            'feature_2082',
                            'feature_2083',
                            'feature_2084',
                            'feature_2085',
                            'feature_2086',
                            'feature_2087',
                            'feature_2088',
                            'feature_2091',
                            'feature_2092',
                            'feature_2093',
                            'feature_2094',
                            'feature_2152',
                            'feature_2154',
                            'feature_2162',
                            'feature_2163',
                            'feature_2170',
                            'feature_2173',
                            'feature_2180',
                            'feature_2182',
                            'feature_2192',
                            'feature_2205',
                            'feature_2233']


        data = self.smiles_to_dataframe(input)

        Y = self.rdkit_fp(data["Smiles"])
        Z = self.rdkit_2d(data["Smiles"])

        data = data.join(Y)
        data = data.join(Z)

        if data.isnull().sum().sum()!=0:
            data=data.dropna()
        #Обработка
        data = shuffle(data)
        data.reset_index(inplace=True)
        X = data.drop(['Smiles',"index"], axis=1)# дроп токо смайлс
        scaler_loaded = joblib.load('..\\models\\scaler_vero.pkl')

        X_scaled = scaler_loaded.transform(X)  # X — это матрица признаков


        # Удаление признаков с низкой дисперсией
        selector_loaded = joblib.load('..\\models\\\selector_vero.pkl')
        X_var_thresh = selector_loaded.transform(X_scaled)
        # Вычислим корреляционную матрицу

        column_names = [f'feature_{i}' for i in range(X_var_thresh.shape[1])]

        to_drop = [column_names.index(col) for col in removed_columns if col in column_names]

        X_uncorr = np.delete(X_var_thresh, to_drop, axis=1)

        # # Сохраним 95% дисперсии данных

        pca_loaded = joblib.load('..\\models\\pca_model_vero.pkl')
        X_pca = pca_loaded.transform(X_uncorr)

        #prediction_v = math.e ** self.model_v.predict(X_pca)
        #print(prediction_v)
        prediction_h =math.e ** self.model_vero.predict(X_pca) - 1e-6
        answer_h = [float(x) for x in prediction_h]
        ##первое число СС50
        return answer_h

    async def proceed_for_virus(self, input : list):
        #Чтение даннных
        removed_columns = [ 'feature_2049',
                            'feature_2055',
                            'feature_2056',
                            'feature_2057',
                            'feature_2061',
                            'feature_2062',
                            'feature_2077',
                            'feature_2078',
                            'feature_2079',
                            'feature_2080',
                            'feature_2081',
                            'feature_2082',
                            'feature_2083',
                            'feature_2084',
                            'feature_2085',
                            'feature_2086',
                            'feature_2087',
                            'feature_2088',
                            'feature_2091',
                            'feature_2092',
                            'feature_2093',
                            'feature_2094',
                            'feature_2126',
                            'feature_2152',
                            'feature_2154',
                            'feature_2162',
                            'feature_2163',
                            'feature_2170',
                            'feature_2173',
                            'feature_2180',
                            'feature_2181',
                            'feature_2182',
                            'feature_2192',
                            'feature_2205',
                            'feature_2233',
                            'feature_2234']


        data = self.smiles_to_dataframe(input)

        Y = self.rdkit_fp(data["Smiles"])
        Z = self.rdkit_2d(data["Smiles"])

        data = data.join(Y)
        data = data.join(Z)

        if data.isnull().sum().sum()!=0:
            data=data.dropna()
        #Обработка
        data = shuffle(data)
        data.reset_index(inplace=True)
        X = data.drop(['Smiles',"index"], axis=1)# дроп токо смайлс
        scaler_loaded = joblib.load('..\\models\\scaler_virus.pkl')

        X_scaled = scaler_loaded.transform(X)  # X — это матрица признаков


        # Удаление признаков с низкой дисперсией
        selector_loaded = joblib.load('..\\models\\selector_virus.pkl')
        X_var_thresh = selector_loaded.transform(X_scaled)
        # Вычислим корреляционную матрицу

        column_names = [f'feature_{i}' for i in range(X_var_thresh.shape[1])]

        to_drop = [column_names.index(col) for col in removed_columns if col in column_names]

        X_uncorr = np.delete(X_var_thresh, to_drop, axis=1)

        # # Сохраним 95% дисперсии данных

        pca_loaded = joblib.load('..\\models\\pca_model_virus.pkl')
        X_pca = pca_loaded.transform(X_uncorr)

        #prediction_v = math.e ** self.model_v.predict(X_pca)
        #print(prediction_v)
        prediction_h =math.e ** self.model_vero.predict(X_pca)
        answer_h = [float(x) for x in prediction_h]
        ## второе число IC50
        return answer_h


    ''''''
    ##SI = CC50/IC50 - третье число  
        