import pandas as pd


def get_data():
    with open('trial_task.json', 'r') as file:
        data = file.read()
        orders_df = pd.read_json(data)
        return orders_df


def tariff_for_warehouse():
    data = get_data()
    tariff_per_warehouse = data.groupby('warehouse_name')['highway_cost'].mean()
    return tariff_per_warehouse


def count_income_expenditure():
    data = get_data()
    orders_expanded_df = data.explode('products')
    orders_expanded_df = pd.concat([orders_expanded_df.drop(['products'], axis=1),
                                    orders_expanded_df['products'].apply(pd.Series)],
                                   axis=1)

    orders_expanded_df['income'] = orders_expanded_df['price'] * orders_expanded_df['quantity']
    orders_expanded_df['expenses'] = orders_expanded_df['highway_cost'] * orders_expanded_df['quantity']
    orders_expanded_df['profit'] = orders_expanded_df['income'] - orders_expanded_df['expenses']

    summary_df = orders_expanded_df.groupby('product').agg({
        'quantity': 'sum',
        'income': 'sum',
        'expenses': 'sum',
        'profit': 'sum'
    }).reset_index()

    return summary_df


def profit_received_from_the_order():
    data = get_data()
    orders_expanded_df = data.explode('products')

    orders_expanded_df = pd.concat(
        [orders_expanded_df.drop(['products'], axis=1),
         orders_expanded_df['products'].apply(pd.Series)],
        axis=1
    )

    orders_expanded_df['income'] = orders_expanded_df['price'] * orders_expanded_df['quantity']
    orders_expanded_df['expenses'] = orders_expanded_df['highway_cost'] * orders_expanded_df['quantity']
    orders_expanded_df['profit'] = orders_expanded_df['income'] - orders_expanded_df['expenses']

    order_profit_df = orders_expanded_df.groupby('order_id')['profit'].sum().reset_index()
    average_profit = order_profit_df['profit'].mean()
    print("Средняя прибыль заказов:", average_profit)
    return order_profit_df


def percent_profit():
    data = get_data()
    product_data = []
    for _, order in data.iterrows():
        warehouse_name = order["warehouse_name"]
        for product_info in order["products"]:
            product_name = product_info["product"]
            quantity = product_info["quantity"]
            price = product_info["price"]
            profit = price * quantity
            product_data.append([warehouse_name, product_name, quantity, profit])

    columns = ["warehouse_name", "product", "quantity", "profit"]
    df = pd.DataFrame(product_data, columns=columns)

    warehouse_profit = df.groupby("warehouse_name")["profit"].sum().reset_index()
    warehouse_profit.rename(columns={"profit": "total_warehouse_profit"}, inplace=True)

    df = pd.merge(df, warehouse_profit, on="warehouse_name")
    df["percent_profit_product_of_warehouse"] = (df["profit"] / df["total_warehouse_profit"]) * 100
    print(df)


def number_fife():
    data = get_data()
    product_data = []
    for _, order in data.iterrows():
        warehouse_name = order["warehouse_name"]
        for product_info in order["products"]:
            product_name = product_info["product"]
            quantity = product_info["quantity"]
            price = product_info["price"]
            profit = price * quantity
            product_data.append([warehouse_name, product_name, quantity, profit])

    columns = ["warehouse_name", "product", "quantity", "profit"]
    df = pd.DataFrame(product_data, columns=columns)

    warehouse_profit = df.groupby("warehouse_name")["profit"].sum().reset_index()
    warehouse_profit.rename(columns={"profit": "total_warehouse_profit"}, inplace=True)

    df = pd.merge(df, warehouse_profit, on="warehouse_name")
    df["percent_profit_product_of_warehouse"] = (df["profit"] / df["total_warehouse_profit"]) * 100
    df.sort_values(by='percent_profit_product_of_warehouse', ascending=False, inplace=True)
    df['accumulated_percent_profit_product_of_warehouse'] = df['percent_profit_product_of_warehouse'].cumsum()

    print(df)


def categorize_accumulated_percent(accumulated_percent):
    if accumulated_percent <= 70:
        return 'A'
    elif 70 < accumulated_percent <= 90:
        return 'B'
    else:
        return 'C'


def number_six():
    data = get_data()
    product_data = []
    for _, order in data.iterrows():
        warehouse_name = order["warehouse_name"]
        for product_info in order["products"]:
            product_name = product_info["product"]
            quantity = product_info["quantity"]
            price = product_info["price"]
            profit = price * quantity
            product_data.append([warehouse_name, product_name, quantity, profit])

    columns = ["warehouse_name", "product", "quantity", "profit"]
    df = pd.DataFrame(product_data, columns=columns)

    warehouse_profit = df.groupby("warehouse_name")["profit"].sum().reset_index()
    warehouse_profit.rename(columns={"profit": "total_warehouse_profit"}, inplace=True)

    df = pd.merge(df, warehouse_profit, on="warehouse_name")
    df["percent_profit_product_of_warehouse"] = (df["profit"] / df["total_warehouse_profit"]) * 100

    df.sort_values(by='percent_profit_product_of_warehouse', ascending=False, inplace=True)
    df['accumulated_percent_profit_product_of_warehouse'] = df['percent_profit_product_of_warehouse'].cumsum()

    df['category'] = df['accumulated_percent_profit_product_of_warehouse'].apply(categorize_accumulated_percent)
    print(df)


number_six()
