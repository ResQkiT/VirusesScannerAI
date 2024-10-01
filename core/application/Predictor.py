import joblib
import pandas as pd
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import Descriptors, AllChem
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import math

class Predictor:
    def __init__(self):
        self.model_v = joblib.load('core\\models\\xgboost_model_virus.joblib')
        self.model_h = joblib.load('core\\models\\xgboost_model_homo.joblib')
        
    
    def smiles_to_dataframe(self, smiles_list):
        print(smiles_list)
        df =  pd.DataFrame({'Smiles': smiles_list})
        print(df)
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
    ''''''

        
    def proceed(self, input : list):
        #Чтение даннных
        data = self.smiles_to_dataframe(input)

        Y = self.rdkit_fp(data["Smiles"])
        Z = self.rdkit_2d(data["Smiles"])
        
        data = data.join(Y)
        data = data.join(Z)
        
        if data.isnull().sum().sum()!=0:
            data=data.dropna()
        print(data)
        #Обработка
        data = shuffle(data)
        data.reset_index(inplace=True)
        X = data.drop(['Smiles',"index"], axis=1)# дроп токо смайлс


        scaler_loaded = joblib.load('core\models\scaler.pkl')
        
        X_scaled = scaler_loaded.transform(X)  # X — это матрица признаков

        # Удаление признаков с низкой дисперсией
        selector_loaded = joblib.load('core\models\selector.pkl')
        X_var_thresh = selector_loaded.transform(X_scaled)
        # Вычислим корреляционную матрицу
        corr_matrix = np.corrcoef(X_scaled, rowvar=False)

        # Удалим признаки, коррелированные выше определенного порога
        upper_triangle = np.triu(np.abs(corr_matrix), k=1)
        to_drop = [i for i in range(upper_triangle.shape[1]) if any(upper_triangle[:, i] > 0.95)]

        X_uncorr = np.delete(X_scaled, to_drop, axis=1)
        print(X_uncorr.shape)
        # Сохраним 95% дисперсии данных


        # weights_loaded = joblib.load('pca_weights.pkl')
        pca_loaded = joblib.load('core\models\pca_weights.joblib')
        X_pca = pca_loaded.transform(X_uncorr)

        #prediction_v = math.e ** self.model_v.predict(X_pca)
        #print(prediction_v)
        prediction_h = math.e ** self.model_h.predict(X_pca)
        print(prediction_h)
        