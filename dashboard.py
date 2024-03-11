import streamlit as st
import pandas as pd

df_orders = pd.read_csv("./dataset/orders_dataset.csv")
df_order_items = pd.read_csv("./dataset/order_items_dataset.csv")
df_order_payments = pd.read_csv("./dataset/order_payments_dataset.csv")
df_order_reviews = pd.read_csv("./dataset/order_reviews_dataset.csv")
df_products = pd.read_csv("./dataset/products_dataset.csv")
df_product_category_name_translation = pd.read_csv(
    "./dataset/product_category_name_translation.csv"
)
df_sellers = pd.read_csv("./dataset/sellers_dataset.csv")
df_geolocation = pd.read_csv("./dataset/geolocation_dataset.csv")
df_customers = pd.read_csv("./dataset/customers_dataset.csv")

# Mengganti nilai baris pada kolom customer_city dalam tabel df_customers
df_customers["customer_city"] = df_customers["customer_city"].apply(lambda x: x.title())

# Mengganti nilai baris pada kolom geolocation_city dalam tabel df_geolocation
df_geolocation["geolocation_city"] = df_geolocation["geolocation_city"].apply(
    lambda x: x.title()
)

# Menghilangkan duplicated rows dengan tetap melakukan konservasi terhadap data pertama yang muncul.
df_geolocation.drop_duplicates(keep="first", inplace=True)

# Menggabungkan tabel df_orders dengan df_order_items
df_order_details = pd.merge(df_orders, df_order_items, how="inner", on="order_id")

# Menambahkan df_order_payments
df_order_details = pd.merge(
    df_order_details, df_order_payments, how="inner", on="order_id"
)

# Menambahkan df_order_reviews
df_order_details = pd.merge(
    df_order_details, df_order_reviews, how="inner", on="order_id"
)

# Mengganti tipe data kolom order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date, shipping_limit_date, review_creation_date, dan review_answer_timestamp
df_order_details["order_purchase_timestamp"] = pd.to_datetime(
    df_order_details["order_purchase_timestamp"]
)
df_order_details["order_approved_at"] = pd.to_datetime(
    df_order_details["order_approved_at"]
)
df_order_details["order_delivered_carrier_date"] = pd.to_datetime(
    df_order_details["order_delivered_carrier_date"]
)
df_order_details["order_delivered_customer_date"] = pd.to_datetime(
    df_order_details["order_delivered_customer_date"]
)
df_order_details["order_estimated_delivery_date"] = pd.to_datetime(
    df_order_details["order_estimated_delivery_date"]
)
df_order_details["shipping_limit_date"] = pd.to_datetime(
    df_order_details["shipping_limit_date"]
)
df_order_details["review_creation_date"] = pd.to_datetime(
    df_order_details["review_creation_date"]
)
df_order_details["review_answer_timestamp"] = pd.to_datetime(
    df_order_details["review_answer_timestamp"]
)

# Mengurutkan produk dengan angka penjualan tertinggi
df_order_product_sell_count = (
    df_order_details.groupby(["product_id"])["order_id"]
    .count()
    .reset_index(name="count")
    .sort_values(["count"], ascending=False)
)

# Buat dataframe baru yang menggabungkan informasi nama kategori produk dengan acuan product_id, kemudian group by product_category_name
df_order_category_sell_count = df_order_details.merge(
    df_products.drop_duplicates(), on="product_id"
).groupby(by="product_category_name")

# Hitung kemunculan masing-masing category dalam kolom baru bernama Count
df_order_category_sell_count = (
    df_order_category_sell_count["order_id"]
    .count()
    .reset_index(name="count")
    .sort_values(["count"], ascending=False)
)

# Setup plotting

# Rename kolom geolocation_zip_code_prefix
df_geolocation.rename(
    columns={"geolocation_zip_code_prefix": "zip_code_prefix"}, inplace=True
)

# Rename kolom customer_zip_code_prefix
df_customers.rename(
    columns={"customer_zip_code_prefix": "zip_code_prefix"}, inplace=True
)

# Ganti tipe data kedua kolom tersebut menjadi string
df_geolocation["zip_code_prefix"] = df_geolocation["zip_code_prefix"].apply(
    lambda x: str(x)
)
df_customers["zip_code_prefix"] = df_customers["zip_code_prefix"].apply(
    lambda x: str(x)
)

# Membuat kolom baru yang menghitung occurrences masing-masing zip_code_prefix pada tabel df_customers
df_customers_zipcode_count = (
    df_customers.groupby("zip_code_prefix")["customer_id"]
    .count()
    .reset_index(name="count")
    .sort_values(["count"], ascending=False)
)

# Merge df_geolocation table to determine its state and city
df_geolocation_customers = df_geolocation.merge(
    df_customers_zipcode_count, on="zip_code_prefix", how="inner"
).drop_duplicates(subset=["zip_code_prefix"])

# Sort value by occurrence count
df_geolocation_customers.sort_values(by="count", ascending=False, inplace=True)

# Group by city and sum the count column, then sort by count
df_geolocation_city_count = (
    df_geolocation_customers.groupby(by="geolocation_city")
    .agg({"count": "sum"})
    .sort_values(by="count", ascending=False)
)

st.write(
    """
    # **Proyek Analisis Data: *E-Commerce Public Dataset***
    - **Nama:** Muhammad Afief Abdurrahman
    - **Email:** M002D4KY1550@bangkit.academy
    - **ID Dicoding:** mafiefa
    ---
    ## Pengenalan dengan dataset yang digunakan
    Dataset yang digunakan diambil dari [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Dataset ini berisi lebih dari 100 ribu informasi mengenai order pada suatu toko bernama *Olist Store*. Periode pengambilan data ini adalah dari tahun 2016 hingga tahun 2018.
    
    ### Skema Dataset
    Berikut adalah skema dari dataset yang digunakan, mengutip dari sumber dataset.
    """
)

st.image(
    "https://i.imgur.com/HRhd2Y0.png",
    caption="Skema Dataset (Sumber: https://i.imgur.com/HRhd2Y0.png)",
)

st.write(
    """
    ## Analisa dataset
    """
)

with st.expander("Pertanyaan 1"):
    st.write(
        """
        ### Bagaimana performa penjualan masing-masing produk dan kategori produk pada periode 2016-2018?
        Berikut adalah hasil dari analisa data yang dilakukan sebelumnya.
        ```notebook
        df_order_product_sell_count.head(10)
        ```
        """
    )

    st.dataframe(df_order_product_sell_count.head(10))

    st.write(
        """
        Dapat dilihat bahwa produk dengan `product_id: aca2eb7d00ea1a7b8ebd4e68314663af` unggul dalam angka penjualan dengan angka 533 penjualan dalam periode 2016-2018. Berikut adalah visualisasi dari penemuan tersebut.
        """
    )

    # Mengganti baris product_id dengan hanya menampilkan 5 karakter pertama
    df_order_product_sell_count["product_id"] = df_order_product_sell_count[
        "product_id"
    ].apply(lambda x: x[0:5])

    df_order_product_sell_count.rename(
        columns={"product_id": "Product ID", "count": "Number of sales"}, inplace=True
    )

    st.bar_chart(
        df_order_product_sell_count.head(10), x="Product ID", y="Number of sales"
    )

    st.write(
        """
        Bagaimana dengan masing-masing kategori produk? Menggunakan dataframe berikut didapat
        ```notebook
        df_order_category_sell_count.head(10)
        ```
        """
    )

    st.dataframe(df_order_category_sell_count.head(10))

    st.write(
        """
        Dapat dilihat bahwa produk dengan kategori `casa_mesa_banho` unggul dalam angka penjualan dengan angka 11847 penjualan dalam periode 2016-2018. Berikut adalah visualisasi dari penemuan tersebut.
        """
    )

    df_order_category_sell_count.rename(
        columns={"product_category_name": "Category", "count": "Number of sales"},
        inplace=True,
    )

    st.bar_chart(
        df_order_category_sell_count.head(10), x="Category", y="Number of sales"
    )


with st.expander("Bagaimana sebaran daerah customer pada periode 2016-2018?"):
    st.write(
        """
        ### Bagaimana daerah sebaran customer pada periode 2016-2018?
        Berikut adalah hasil dari analisa data yang dilakukan sebelumnya.
        ```notebook
        df_geolocation_city_count.head()
        ```
        """
    )

    st.dataframe(df_geolocation_city_count.head())

    st.bar_chart(df_geolocation_city_count.head())
