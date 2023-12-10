{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a47d583a-00de-4059-ad1e-e5dfb9760835",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from datetime import time\n",
    "\n",
    "\n",
    "#Question 1: Distance Matrix Calculation\n",
    "def calculate_distance_matrix(dataset_path):\n",
    "    distances = {}                                                               #Empyt dictionary\n",
    "    for index, row in df.iterrows():\n",
    "        start_location = row.id_start\n",
    "        end_location = row.id_end\n",
    "        distance = row.distance\n",
    "        distances[(start_location, end_location)] = distance\n",
    "        distances[(end_location, start_location)] = distance\n",
    "    toll_locations = df.id_start.unique()\n",
    "    distance_matrix = pd.DataFrame(0, index=toll_locations, columns=toll_locations)\n",
    "    for i in toll_locations:\n",
    "        for j in toll_locations:\n",
    "            if i != j:\n",
    "                direct_distance = distances.get((i, j), None)\n",
    "                if direct_distance is not None:\n",
    "                    distance_matrix.loc[i, j] = direct_distance\n",
    "                else:\n",
    "                    for k in toll_locations:\n",
    "                        if i != k and j != k:\n",
    "                            cumulative_distance = distance_matrix.loc[i, k] + distance_matrix.loc[k, j]\n",
    "                            if distance_matrix.loc[i, j] == 0 or cumulative_distance < distance_matrix.loc[i, j]:\n",
    "                                distance_matrix.loc[i, j] = cumulative_distance\n",
    "\n",
    "    return distance_matrix\n",
    "\n",
    "dataset = 'dataset-3.csv'\n",
    "resulting_matrix = calculate_distance_matrix(dataset)\n",
    "print(resulting_matrix)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "#Question 2: Unroll Distance Matrix\n",
    "def unroll_distance_matrix(distance_matrix):\n",
    "    upper_triangle = distance_matrix.where(np.triu(np.ones(distance_matrix.shape), k=1).astype(bool))\n",
    "    unrolled_df = upper_triangle.stack().reset_index()\n",
    "    unrolled_df.columns = ['id_start', 'id_end', 'distance']\n",
    "\n",
    "    return unrolled_df\n",
    "\n",
    "unrolled_df = unroll_distance_matrix(resulting_matrix)\n",
    "print(unrolled_df)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "#Question 3: Finding IDs within Percentage Threshold\n",
    "def find_ids_within_ten_percentage_threshold(df, reference_value):\n",
    "    reference_rows = df[df['id_start'] == reference_value]\n",
    "    average_distance = reference_rows['distance'].mean()\n",
    "    lower_threshold = average_distance - 0.1 * average_distance\n",
    "    upper_threshold = average_distance + 0.1 * average_distance\n",
    "    within_threshold_rows = df[(df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]\n",
    "    result_ids = sorted(within_threshold_rows['id_start'].unique())\n",
    "\n",
    "    return result_ids\n",
    "\n",
    "reference_value = 1001468  # Taking last index value of id_start column as an integer\n",
    "result_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)\n",
    "print(result_ids)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "#Question 4: Calculate Toll Rate\n",
    "def calculate_toll_rate(df):\n",
    "    #Parsing values for keys\n",
    "    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}\n",
    "\n",
    "    for vehicle_type, rate_coefficient in rate_coefficients.items():\n",
    "        df['vehicle_type'] = df.distance * rate_coefficient\n",
    "    return df\n",
    "\n",
    "result_with_toll_rates = calculate_toll_rate(unrolled_df)\n",
    "print(result_with_toll_rates)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "#Question 5: Calculate Time-Based Toll Rates\n",
    "def calculate_time_based_toll_rates(df):\n",
    "    time_ranges_weekdays = [(time(0, 0, 0), time(10, 0, 0)),\n",
    "                            (time(10, 0, 0), time(18, 0, 0)),\n",
    "                            (time(18, 0, 0), time(23, 59, 59))]\n",
    "\n",
    "    time_ranges_weekends = [(time(0, 0, 0), time(23, 59, 59))]\n",
    "    df['start_day'] = df['end_day'] = df['start_time'] = df['end_time'] = None\n",
    "\n",
    "    def map_time_range(start, end, time_ranges):\n",
    "        for time_range in time_ranges:\n",
    "            if start >= time_range[0] and end <= time_range[1]:\n",
    "                return time_range\n",
    "        return None\n",
    "\n",
    "    def apply_time_based_rates(row, time_ranges, discount_factor):\n",
    "        start_day = row['start_day']\n",
    "        end_day = row['end_day']\n",
    "        start_time = row['start_time']\n",
    "        end_time = row['end_time']\n",
    "\n",
    "        for time_range in time_ranges:\n",
    "            if start_time >= time_range[0] and end_time <= time_range[1]:\n",
    "                row['start_time'] = time_range[0]\n",
    "                row['end_time'] = time_range[1]\n",
    "                row['start_day'] = start_day\n",
    "                row['end_day'] = end_day\n",
    "                row[['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor\n",
    "                return row\n",
    "\n",
    "    for index, row in df.iterrows():\n",
    "        start_day = row['start_day']\n",
    "        end_day = row['end_day']\n",
    "\n",
    "        if start_day == end_day:\n",
    "            if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']: \n",
    "                #we can also put if start_day in ['Saturday', 'Sunday']: --> else :\n",
    "                row = apply_time_based_rates(row, time_ranges_weekdays, 0.8)\n",
    "            elif start_day in ['Saturday', 'Sunday']:\n",
    "                row = apply_time_based_rates(row, time_ranges_weekends, 0.7)\n",
    "\n",
    "    return df\n",
    "\n",
    "result_with_time_based_rates = calculate_time_based_toll_rates(result_with_toll_rates)\n",
    "print(result_with_time_based_rates)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
