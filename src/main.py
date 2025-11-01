from load_dataset import load_crop_data
from  gps_and_oc_generator import gps_generator
from  gps_and_oc_generator import oc_generator
from theoritical_sfi import sfi_dataset
from random_forest_model import rf_model
from fertility_map import analysis_window
from fertility_map import fertility_map

def main():
    data = load_crop_data()
    
    data = gps_generator(data, field_size_m=1000)

    data = oc_generator(data)

    data = sfi_dataset(data)

    model, features, r2_train, r2_test, rmse, feat_import = rf_model(data)
    print("\n-----------Random Forest Model Results---------")
    print(f"R2 Train: {r2_train:.4f}")
    print(f"R2 Test: {r2_test:.4f}")
    print(f"RMSE : {r2_train:.4f}")
    print("\nFeature Importance:")
    for feat, imp in feat_import.items():
        print(f"{feat}: {imp:.4f}")

    fertility_map(data, resolution=100)

    analysis_window(data)

if __name__ == "__main__":
    main()
