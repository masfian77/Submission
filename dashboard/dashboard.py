import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english")["order_id"].nunique().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={"order_id": "number_of_sales"}, inplace=True)  # Rename for clarity
    return sum_order_items_df

def create_review_score_df(df):
        review_score_df = df['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_score_df.idxmax()
        df_cust=df['review_score']

        return (review_score_df, most_common_score, df_cust)

# Load your data
all_df = pd.read_csv("../all_data.csv")

st.header('E-Commerce Public Dataset :sparkles:')
st.subheader("Best & Worst Performing Product")

# Call this function to create the DataFrame
sum_order_items_df = create_sum_order_items_df(all_df)
review_score_df,most_common_score_df,df_cust_df = create_review_score_df(all_df)  

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Best Performing Product
sns.barplot(x="number_of_sales", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=20)
ax[0].set_title("Best Performing Product", loc="center", fontsize=25)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

# Worst Performing Product
sns.barplot(x="number_of_sales", y="product_category_name_english", data=sum_order_items_df.sort_values(by="number_of_sales", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=25)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Review Score
st.subheader("Rating & Review Score")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"Average Review Score: **{df_cust_df.mean():.2f}**")

with col2:
    st.markdown(f"Most Common Review Score: **{df_cust_df.value_counts().idxmax()}**")

fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("viridis", len(review_score_df))

sns.barplot(x=review_score_df.index,
            y=review_score_df.values,
            order=review_score_df.index,
            palette=colors)

plt.title("Customer Review Scores for Service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

for i, v in enumerate(review_score_df.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig)

st.subheader("Fitur Interaktif Rating & Review Score")

# Filter by rating using a selectbox
rating_filter = st.selectbox(
    'Filter by Rating Score',
    options=[None] + sorted(df_cust_df.unique().tolist()),
    index=0
)

# Filter the dataframe based on the selected rating
if rating_filter is not None:
    filtered_df = df_cust_df[df_cust_df == rating_filter]
else:
    filtered_df = df_cust_df

# Display the Average and Most Common Review Score based on the filtered data
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"Average Review Score: **{filtered_df.mean():.2f}**")

with col2:
    st.markdown(f"Most Common Review Score: **{filtered_df.value_counts().idxmax()}**")

# Count the occurrences of each rating in the filtered data
review_score_df_filtered = filtered_df.value_counts().sort_index()

# Create a bar plot for the filtered data
fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("viridis", len(review_score_df_filtered))

sns.barplot(x=review_score_df_filtered.index,
            y=review_score_df_filtered.values,
            order=review_score_df_filtered.index,
            palette=colors)

plt.title("Customer Review Scores for Service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

for i, v in enumerate(review_score_df_filtered.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig)    