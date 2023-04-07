import pandas as pd
import pickle
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

values_with_property_area = pd.read_csv('def_values.csv')


def cal_Furnishing_Equivalent(Furnishing):
    if Furnishing == "Unfurnished":
        Furnishing_equivalent = 3
    if Furnishing == "NA":
        Furnishing_equivalent = 1.5
    if Furnishing == "Semi_Furnished":
        Furnishing_equivalent = 2
    if Furnishing == "Fully Furnished":
        Furnishing_equivalent = 1
    return Furnishing_equivalent


def cal_Prop_Type_Equivalent(Property_Type):
    if Property_Type == "Bungalow":
        Property_Type_equivalent = 6
    if Property_Type == "Duplex":
        Property_Type_equivalent = 5
    if Property_Type == "#R%$G&867":
        Property_Type_equivalent = 3
    if Property_Type == "Single-family home":
        Property_Type_equivalent = 4
    if Property_Type == "Apartment":
        Property_Type_equivalent = 2
    if Property_Type == "Container Home":
        Property_Type_equivalent = 1
    return Property_Type_equivalent


def fill_df(Property_Area, Number_of_Windows, Number_of_Doors, Furnishing_equivalent, Property_Type_equivalent):
    Frequency_of_Powercuts = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Frequency_of_Powercuts'].mean()
    Traffic_Density_Score = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Traffic_Density_Score'].mean()
    Air_Quality_Index = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Air_Quality_Index'].mean()
    Neighborhood_Review = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Neighborhood_Review'].mean()
    Crime_Rate_equivalent = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Crime_Rate_equivalent'].mean()
    Water_Supply_equivalent = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Water_Supply_equivalent'].mean()
    Dust_and_Noise_equivalent = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Dust_and_Noise_equivalent'].mean()
    Power_Backup_equivalent = values_with_property_area.loc[values_with_property_area[
        'Property_Area'] == Property_Area, 'Power_Backup_equivalent'].mean()

#   data_list = [Property_Area,
#  Number_of_Windows,
#  Number_of_Doors,
#  Frequency_of_Powercuts,
#  Traffic_Density_Score,
#  Air_Quality_Index,
#  Neighborhood_Review,
#  Crime_Rate_equivalent,
#  Water_Supply_equivalent,
#  Dust_and_Noise_equivalent,
#  Furnishing_equivalent,
#  Property_Type_equivalent,
#  Power_Backup_equivalent]

    data_dict = data = {'Property_Area': [Property_Area],
                        'Number_of_Windows': [Number_of_Windows],
                        'Number_of_Doors': [Number_of_Doors],
                        'Frequency_of_Powercuts': [Frequency_of_Powercuts],
                        'Traffic_Density_Score': [Traffic_Density_Score],
                        'Air_Quality_Index': [Air_Quality_Index],
                        'Neighborhood_Review': [Neighborhood_Review],
                        'Crime_Rate_equivalent': Crime_Rate_equivalent,
                        'Water_Supply_equivalent': [Water_Supply_equivalent],
                        'Dust_and_Noise_equivalent': [Dust_and_Noise_equivalent],
                        'Furnishing_equivalent': [Furnishing_equivalent],
                        'Property_Type_equivalent': [Property_Type_equivalent],
                        'Power_Backup_equivalent': [Power_Backup_equivalent]}

    pred_df = pd.DataFrame(data_dict)
    return pred_df


def cal_habitability(Property_Area, Number_of_Windows, Number_of_Doors, Furnishing, Property_Type):
    Furnishing_equivalent = cal_Furnishing_Equivalent(Furnishing)
    Property_Type_equivalent = cal_Prop_Type_Equivalent(Property_Type)
    if Property_Area in values_with_property_area['Property_Area'].unique():
        pred_df = fill_df(Property_Area, Number_of_Windows, Number_of_Doors,
                          Furnishing_equivalent, Property_Type_equivalent)
    else:
        def_dict = {
            'Property_Area': [Property_Area],
            'Number_of_Windows': [Number_of_Windows],
            'Number_of_Doors': [Number_of_Doors],
            'Frequency_of_Powercuts': [values_with_property_area['Frequency_of_Powercuts'].mean()],
            'Traffic_Density_Score': [values_with_property_area['Traffic_Density_Score'].mean()],
            'Air_Quality_Index': [values_with_property_area['Air_Quality_Index'].mean()],
            'Neighborhood_Review': [values_with_property_area['Neighborhood_Review'].mean()],
            'Crime_Rate_equivalent': [values_with_property_area['Crime_Rate_equivalent'].mean()],
            'Water_Supply_equivalent': [values_with_property_area['Water_Supply_equivalent'].mean()],
            'Dust_and_Noise_equivalent': [values_with_property_area['Dust_and_Noise_equivalent'].mean()],
            'Furnishing_equivalent': [Furnishing_equivalent],
            'Property_Type_equivalent': [Property_Type_equivalent],
            'Power_Backup_equivalent': [values_with_property_area['Power_Backup_equivalent'].mean()]}
        pred_df = pd.DataFrame(def_dict)
    prediction = loaded_model.predict(pred_df)
    return {"habitability": float(prediction[0])}
