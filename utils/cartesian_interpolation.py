import numpy as np

def interpolate_waterfront_cartesian(df, distance_threshold=0.0015):
    """
    Interpolate waterfront using simple Euclidean distance on lat/long.

    Parameters:
    - distance_threshold: degrees (~0.0015 degrees ≈ 165 m)

    Returns: DataFrame with imputed values
    """
    df = df.copy()

    # Separate known and unknown
    df_known = df[df['waterfront'].notna()].copy()
    df_unknown = df[df['waterfront'].isna()].copy()

    print(f"\nKnown waterfront: {len(df_known)}")
    print(f"Unknown waterfront: {len(df_unknown)}")

    imputed_values = []
    imputation_info = []

    # For each property with unknown waterfront
    for idx, row in df_unknown.iterrows():
        lat = row['latitude']
        lon = row['longitude']

        # Calculate Euclidean distance to all known properties
        # Simple formula: sqrt((lat1-lat2)^2 + (lon1-lon2)^2)
        df_known['distance'] = np.sqrt(
            (df_known['latitude'] - lat)**2 +
            (df_known['longitude'] - lon)**2
        )

        # Find neighbors within threshold
        neighbors = df_known[df_known['distance'] <= distance_threshold]

        if len(neighbors) == 0:
            # No neighbors found - use mode (most common value)
            imputed = df_known['waterfront'].mode()[0]
            imputation_method = 'mode_fallback'
        else:
            # Use majority vote from neighbors
            waterfront_mean = neighbors['waterfront'].mean()
            imputed = 1 if waterfront_mean > 0.5 else 0
            imputation_method = f'{len(neighbors)}_neighbors'

        imputed_values.append(imputed)
        imputation_info.append({
            'id': row['id'],
            'latitude': lat,
            'longitude': lon,
            'imputed_waterfront': imputed,
            'method': imputation_method,
            'n_neighbors': len(neighbors) if len(neighbors) > 0 else 0
        })

    # Update the dataframe
    df.loc[df_unknown.index, 'waterfront'] = imputed_values

    print(f"\nImputation complete!")
    print(f"Imputed as waterfront=1: {sum(np.array(imputed_values) == 1)}")
    print(f"Imputed as waterfront=0: {sum(np.array(imputed_values) == 0)}")

    return df

