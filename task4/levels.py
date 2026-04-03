"""
Level definitions for SQL Learning Game.
Contains all 5 levels with story, challenges, hints, and expected results.
"""
from task4.game_logic import Level, Challenge
from task4.database import execute_query

from pathlib import Path

# Level images (stored locally in task4/images folder)
_images_dir = Path(__file__).parent / "images"
LEVEL_IMAGES = {
    1: str(_images_dir / "restaurant.jpg"),  # Restaurant interior
    2: str(_images_dir / "charts.jpg"),      # Charts and analytics
    3: str(_images_dir / "money.jpg"),       # Calculator/money
    4: str(_images_dir / "network.jpg"),     # Connection/network
    5: str(_images_dir / "hacker.jpg")       # Mysterious/hacker
}


def create_all_levels():
    """Create and return all 5 game levels with challenges."""
    levels = []
    
    # ========================================
    # LEVEL 1: SELECT & WHERE
    # ========================================
    level1 = Level(
        number=1,
        title="🍽️ Welcome to Your Restaurant!",
        story_intro="""
Welcome, future restaurant mogul! 🎉

You've just opened your dream restaurant, and business is booming! But you're overwhelmed with data—hundreds of orders, different payment methods, countless menu items...

**Your mission:** Learn SQL to understand your business better. Let's start with the basics: viewing and filtering data.

### What You'll Learn:
- 📋 `SELECT` - Choose which data to view
- 🔍 `WHERE` - Filter data based on conditions
- 🎯 `AND`/`OR` - Combine multiple conditions

### Your Database:
You have an `orders` table with these columns:
- `order_id` - Unique order number
- `customer_name` - Who ordered
- `food_item` - What they ordered (Pizza, Burger, Pasta, etc.)
- `category` - Type of food (Main, Dessert, Starter)
- `quantity` - How many items
- `price` - Price per item
- `payment_method` - How they paid (Cash, Credit Card, Debit Card, Online Payment)
- `order_time` - When they ordered

Let's dive in! 🏊‍♂️
        """,
        story_outro="""
🎊 **Congratulations!** You've mastered the basics of SELECT and WHERE!

You can now view your data and filter it to find exactly what you need. These are the foundation of SQL—you'll use them in EVERY query you write.

**Next up:** Let's learn how to sort and limit results to find your top performers! 📊
        """,
        teaches_concepts=["SELECT", "WHERE", "AND", "OR", "LIMIT"]
    )
    
    # Challenge 1.1: Basic SELECT
    level1.add_challenge(Challenge(
        question="**Challenge 1:** Let's see your data! Write a query to view the first 10 orders from your database. Use `SELECT * FROM orders LIMIT 10`",
        expected_result=execute_query("SELECT * FROM orders LIMIT 10"),
        expected_query="SELECT * FROM orders LIMIT 10",
        hint_1="Start with SELECT * to select all columns, then FROM orders to specify the table, and LIMIT 10 to show only 10 rows.",
        hint_2="The complete query is: SELECT * FROM orders LIMIT 10",
        hint_3="Copy this exactly: SELECT * FROM orders LIMIT 10"
    ))
    
    # Challenge 1.2: Filter by specific item
    level1.add_challenge(Challenge(
        question="**Challenge 2:** Find all Pizza orders. Filter the orders where `food_item` equals 'Pizza'.",
        expected_result=execute_query("SELECT * FROM orders WHERE food_item = 'Pizza'"),
        expected_query="SELECT * FROM orders WHERE food_item = 'Pizza'",
        hint_1="Use WHERE to filter. The syntax is: WHERE column_name = 'value'",
        hint_2="You need: SELECT * FROM orders WHERE food_item = 'Pizza'",
        hint_3="SELECT * FROM orders WHERE food_item = 'Pizza'"
    ))
    
    # Challenge 1.3: Filter by category
    level1.add_challenge(Challenge(
        question="**Challenge 3:** Show all Dessert orders. The category column tells you if something is a Main, Dessert, or Starter.",
        expected_result=execute_query("SELECT * FROM orders WHERE category = 'Dessert'"),
        expected_query="SELECT * FROM orders WHERE category = 'Dessert'",
        hint_1="Similar to the last challenge, but filter by category instead of food_item.",
        hint_2="Use: WHERE category = 'Dessert'",
        hint_3="SELECT * FROM orders WHERE category = 'Dessert'"
    ))
    
    # Challenge 1.4: Multiple conditions with AND
    level1.add_challenge(Challenge(
        question="**Challenge 4:** Find Main course orders with quantity greater than 3. Use AND to combine two conditions.",
        expected_result=execute_query("SELECT * FROM orders WHERE category = 'Main' AND quantity > 3"),
        expected_query="SELECT * FROM orders WHERE category = 'Main' AND quantity > 3",
        hint_1="You need two conditions: category = 'Main' AND quantity > 3. Combine them with AND.",
        hint_2="The syntax is: WHERE condition1 AND condition2",
        hint_3="SELECT * FROM orders WHERE category = 'Main' AND quantity > 3"
    ))
    
    # Challenge 1.5: Choose specific columns
    level1.add_challenge(Challenge(
        question="**Challenge 5:** Instead of `SELECT *`, choose specific columns. Show only `customer_name`, `food_item`, and `price` for all orders.",
        expected_result=execute_query("SELECT customer_name, food_item, price FROM orders"),
        expected_query="SELECT customer_name, food_item, price FROM orders",
        hint_1="Replace the * with column names separated by commas: SELECT column1, column2, column3 FROM orders",
        hint_2="You need: SELECT customer_name, food_item, price FROM orders",
        hint_3="SELECT customer_name, food_item, price FROM orders"
    ))
    
    levels.append(level1)
    
    # ========================================
    # LEVEL 2: ORDER BY & LIMIT
    # ========================================
    level2 = Level(
        number=2,
        title="📊 Find Your Best & Worst Performers",
        story_intro="""
Great work! Now you can view and filter your data. 🎯

But as a business owner, you need to answer questions like:
- "What are my most expensive orders?"
- "Which were my first orders?"
- "What are my cheapest menu items?"

To answer these, you need to **sort** your data!

### What You'll Learn:
- 🔼 `ORDER BY` - Sort results
- 🔽 `DESC` / `ASC` - Sort direction (descending/ascending)
- 🎯 `LIMIT` - Show only top N results

**Pro tip:** Combine ORDER BY with LIMIT to find "Top 5" or "Bottom 10" results!
        """,
        story_outro="""
🌟 **Excellent!** You can now sort data and find top/bottom performers!

These skills are crucial for business analytics. Want to find your best customers? Top-selling items? Oldest inventory? ORDER BY is your friend!

**Coming up:** Aggregations—calculating totals, averages, and counts! 🧮
        """,
        teaches_concepts=["ORDER BY", "DESC", "ASC", "LIMIT"]
    )
    
    # Challenge 2.1: Order by price descending
    level2.add_challenge(Challenge(
        question="**Challenge 1:** Find your top 5 most expensive orders. Sort by `price` in descending order (highest first) and limit to 5 results.",
        expected_result=execute_query("SELECT * FROM orders ORDER BY price DESC LIMIT 5"),
        expected_query="SELECT * FROM orders ORDER BY price DESC LIMIT 5",
        hint_1="Use ORDER BY price DESC to sort by price (highest first), then add LIMIT 5",
        hint_2="Combine: SELECT * FROM orders ORDER BY price DESC LIMIT 5",
        hint_3="SELECT * FROM orders ORDER BY price DESC LIMIT 5"
    ))
    
    # Challenge 2.2: Order by time ascending
    level2.add_challenge(Challenge(
        question="**Challenge 2:** Show your first 10 orders chronologically. Sort by `order_time` in ascending order (oldest first).",
        expected_result=execute_query("SELECT * FROM orders ORDER BY order_time ASC LIMIT 10"),
        expected_query="SELECT * FROM orders ORDER BY order_time ASC LIMIT 10",
        hint_1="Use ORDER BY order_time ASC (ASC means ascending, oldest first)",
        hint_2="You need: SELECT * FROM orders ORDER BY order_time ASC LIMIT 10",
        hint_3="SELECT * FROM orders ORDER BY order_time ASC LIMIT 10"
    ))
    
    # Challenge 2.3: Filter and sort
    level2.add_challenge(Challenge(
        question="**Challenge 3:** Find the cheapest Desserts. Filter WHERE category = 'Dessert', then sort by price ascending.",
        expected_result=execute_query("SELECT * FROM orders WHERE category = 'Dessert' ORDER BY price ASC"),
        expected_query="SELECT * FROM orders WHERE category = 'Dessert' ORDER BY price ASC",
        hint_1="Combine WHERE and ORDER BY: first filter (WHERE category = 'Dessert'), then sort (ORDER BY price ASC)",
        hint_2="The order is: SELECT ... FROM ... WHERE ... ORDER BY ...",
        hint_3="SELECT * FROM orders WHERE category = 'Dessert' ORDER BY price ASC"
    ))
    
    # Challenge 2.4: Sort by multiple columns
    level2.add_challenge(Challenge(
        question="**Challenge 4:** Show orders sorted by category first, then by price (highest to lowest). Use `ORDER BY category, price DESC`.",
        expected_result=execute_query("SELECT * FROM orders ORDER BY category, price DESC"),
        expected_query="SELECT * FROM orders ORDER BY category, price DESC",
        hint_1="You can sort by multiple columns: ORDER BY column1, column2 DESC",
        hint_2="First sort by category (alphabetically), then by price descending within each category",
        hint_3="SELECT * FROM orders ORDER BY category, price DESC"
    ))
    
    levels.append(level2)
    
    # ========================================
    # LEVEL 3: GROUP BY & AGGREGATIONS
    # ========================================
    level3 = Level(
        number=3,
        title="🧮 Calculate Revenue & Find Patterns",
        story_intro="""
Fantastic progress! You can now view, filter, and sort your data. 💪

But here's the million-dollar question: **"How much money am I making?"**

To answer this, you need to **aggregate**—calculate sums, averages, counts, etc.

### What You'll Learn:
- 📊 `COUNT()` - Count rows
- 💰 `SUM()` - Add up values
- 📈 `AVG()` - Calculate average
- 🔝 `MAX()` / `MIN()` - Find highest/lowest
- 📦 `GROUP BY` - Group rows and calculate per group

**Example:** Instead of seeing 500 individual orders, see "How many orders per category?"

Let's calculate some business metrics! 💼
        """,
        story_outro="""
🎉 **Amazing!** You're now a data analyst!

You can calculate totals, averages, and grouped statistics. These are the queries that help businesses make decisions!

**Next:** JOIN tables together to combine different data sources! 🔗
        """,
        teaches_concepts=["COUNT", "SUM", "AVG", "MAX", "MIN", "GROUP BY", "HAVING"]
    )
    
    # Challenge 3.1: Total revenue
    level3.add_challenge(Challenge(
        question="**Challenge 1:** Calculate your total revenue! Each order's revenue is `price * quantity`. Use `SUM(price * quantity)` to add them all up. Give it an alias: `AS total_revenue`",
        expected_result=execute_query("SELECT SUM(price * quantity) AS total_revenue FROM orders"),
        expected_query="SELECT SUM(price * quantity) AS total_revenue FROM orders",
        hint_1="Use SUM() to add values. You can do math inside: SUM(price * quantity)",
        hint_2="The syntax is: SELECT SUM(price * quantity) AS total_revenue FROM orders",
        hint_3="SELECT SUM(price * quantity) AS total_revenue FROM orders"
    ))
    
    # Challenge 3.2: Count orders per category
    level3.add_challenge(Challenge(
        question="**Challenge 2:** How many orders per category? Use `GROUP BY category` and `COUNT(*)` to count rows in each group.",
        expected_result=execute_query("SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category"),
        expected_query="SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category",
        hint_1="When you GROUP BY a column, you see one row per unique value. COUNT(*) counts rows in each group.",
        hint_2="SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category",
        hint_3="SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category"
    ))
    
    # Challenge 3.3: Average order value
    level3.add_challenge(Challenge(
        question="**Challenge 3:** What's your average order value? Calculate `AVG(price * quantity)` as `avg_order_value`.",
        expected_result=execute_query("SELECT AVG(price * quantity) AS avg_order_value FROM orders"),
        expected_query="SELECT AVG(price * quantity) AS avg_order_value FROM orders",
        hint_1="AVG() calculates the mean. Use AVG(price * quantity) to get average order value.",
        hint_2="SELECT AVG(price * quantity) AS avg_order_value FROM orders",
        hint_3="SELECT AVG(price * quantity) AS avg_order_value FROM orders"
    ))
    
    # Challenge 3.4: Most popular food items
    level3.add_challenge(Challenge(
        question="**Challenge 4:** Find your 5 most popular food items by order count. Group by `food_item`, count orders, sort descending, limit 5.",
        expected_result=execute_query("SELECT food_item, COUNT(*) AS order_count FROM orders GROUP BY food_item ORDER BY order_count DESC LIMIT 5"),
        expected_query="SELECT food_item, COUNT(*) AS order_count FROM orders GROUP BY food_item ORDER BY order_count DESC LIMIT 5",
        hint_1="Combine GROUP BY, COUNT(), ORDER BY, and LIMIT: group by food_item, count, sort by count descending, limit to 5.",
        hint_2="SELECT food_item, COUNT(*) AS order_count FROM orders GROUP BY food_item ORDER BY order_count DESC LIMIT 5",
        hint_3="SELECT food_item, COUNT(*) AS order_count FROM orders GROUP BY food_item ORDER BY order_count DESC LIMIT 5"
    ))
    
    # Challenge 3.5: Revenue by payment method
    level3.add_challenge(Challenge(
        question="**Challenge 5:** Calculate total revenue per payment method. Group by `payment_method` and sum `price * quantity`.",
        expected_result=execute_query("SELECT payment_method, COUNT(*) AS order_count, SUM(price * quantity) AS revenue FROM orders GROUP BY payment_method"),
        expected_query="SELECT payment_method, COUNT(*) AS order_count, SUM(price * quantity) AS revenue FROM orders GROUP BY payment_method",
        hint_1="You can use multiple aggregations: COUNT(*) and SUM(price * quantity) in the same query.",
        hint_2="SELECT payment_method, COUNT(*) AS order_count, SUM(price * quantity) AS revenue FROM orders GROUP BY payment_method",
        hint_3="SELECT payment_method, COUNT(*) AS order_count, SUM(price * quantity) AS revenue FROM orders GROUP BY payment_method"
    ))
    
    levels.append(level3)
    
    # ========================================
    # LEVEL 4: JOIN
    # ========================================
    level4 = Level(
        number=4,
        title="🔗 Combine Tables with JOIN",
        story_intro="""
You're doing great! But here's the thing... 🤔

Real businesses have data spread across MULTIPLE tables. You have:
- `orders` table - customer orders
- `food_items` table - menu items with cost_to_make and profit_margin

To calculate profit, you need to combine them!

### What You'll Learn:
- 🔗 `JOIN` - Combine tables based on matching columns
- 🎯 `ON` - Specify which columns to match
- 💡 `table.column` - Specify which table a column comes from

**Example:** Join orders with food_items ON orders.food_item = food_items.food_item

Let's unlock deeper insights! 🚀
        """,
        story_outro="""
🏆 **Incredible!** You've mastered JOIN—one of SQL's most powerful features!

You can now combine data from multiple sources to create rich, insightful reports. This is what separates beginners from SQL pros!

**But wait...** Something terrible is about to happen... 😱
        """,
        teaches_concepts=["JOIN", "INNER JOIN", "ON", "table.column syntax"]
    )
    
    # Challenge 4.1: Basic JOIN
    level4.add_challenge(Challenge(
        question="**Challenge 1:** Join the `orders` and `food_items` tables. Show order_id, food_item, price, and cost_to_make. Use `JOIN food_items ON orders.food_item = food_items.food_item`",
        expected_result=execute_query("SELECT orders.order_id, orders.food_item, orders.price, food_items.cost_to_make FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10"),
        expected_query="SELECT orders.order_id, orders.food_item, orders.price, food_items.cost_to_make FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10",
        hint_1="Use JOIN to combine tables: FROM orders JOIN food_items ON orders.food_item = food_items.food_item",
        hint_2="SELECT orders.order_id, orders.food_item, orders.price, food_items.cost_to_make FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10",
        hint_3="SELECT orders.order_id, orders.food_item, orders.price, food_items.cost_to_make FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10"
    ))
    
    # Challenge 4.2: Calculate profit per order
    level4.add_challenge(Challenge(
        question="**Challenge 2:** Calculate profit per order! Profit = (price - cost_to_make) * quantity. Join the tables and calculate this for each order.",
        expected_result=execute_query("SELECT orders.order_id, orders.food_item, (orders.price - food_items.cost_to_make) * orders.quantity AS profit FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10"),
        expected_query="SELECT orders.order_id, orders.food_item, (orders.price - food_items.cost_to_make) * orders.quantity AS profit FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10",
        hint_1="You can do math with joined columns: (orders.price - food_items.cost_to_make) * orders.quantity",
        hint_2="SELECT orders.order_id, orders.food_item, (orders.price - food_items.cost_to_make) * orders.quantity AS profit FROM orders JOIN food_items ON ...",
        hint_3="SELECT orders.order_id, orders.food_item, (orders.price - food_items.cost_to_make) * orders.quantity AS profit FROM orders JOIN food_items ON orders.food_item = food_items.food_item LIMIT 10"
    ))
    
    # Challenge 4.3: Most profitable food item
    level4.add_challenge(Challenge(
        question="**Challenge 3:** Which food item generates the most profit? Join tables, group by food_item, sum profit, and find the top one!",
        expected_result=execute_query("SELECT orders.food_item, SUM((orders.price - food_items.cost_to_make) * orders.quantity) AS total_profit FROM orders JOIN food_items ON orders.food_item = food_items.food_item GROUP BY orders.food_item ORDER BY total_profit DESC LIMIT 1"),
        expected_query="SELECT orders.food_item, SUM((orders.price - food_items.cost_to_make) * orders.quantity) AS total_profit FROM orders JOIN food_items ON orders.food_item = food_items.food_item GROUP BY orders.food_item ORDER BY total_profit DESC LIMIT 1",
        hint_1="Combine JOIN, GROUP BY, SUM, ORDER BY, and LIMIT! Group by food_item, sum the profit, sort descending, limit 1.",
        hint_2="SELECT orders.food_item, SUM((price - cost_to_make) * quantity) AS total_profit FROM orders JOIN food_items ON ... GROUP BY orders.food_item ORDER BY total_profit DESC LIMIT 1",
        hint_3="SELECT orders.food_item, SUM((orders.price - food_items.cost_to_make) * orders.quantity) AS total_profit FROM orders JOIN food_items ON orders.food_item = food_items.food_item GROUP BY orders.food_item ORDER BY total_profit DESC LIMIT 1"
    ))
    
    levels.append(level4)
    
    # ========================================
    # LEVEL 5: THE SABOTAGE (INSERT/UPDATE)
    # ========================================
    level5 = Level(
        number=5,
        title="😈 SABOTAGE TIME!",
        story_intro="""
## 🚨 BREAKING NEWS 🚨

Your mean uncle just walked in and... **STOLE YOUR RESTAURANT!** 😱

He's kicked you out and claims he'll run it "better than you ever did." He's about to analyze YOUR data to make HIS business decisions.

But you still have database access... 😏

### Your Mission:
**Sabotage the data to completely mislead your uncle!**

Make his analysis so wrong that he runs the business into the ground!

### What You'll Learn:
- 💣 `INSERT` - Add fake records
- 🔧 `UPDATE` - Modify existing data
- 😈 Chaos and revenge!

**Warning:** You're about to break things. But that's the point! Let's make your uncle regret stealing your restaurant! 💀  
When you finished you can reset the game and data using the button in the left sidebar.
        """,
        story_outro="""
## 🎉 MISSION ACCOMPLISHED! 🎉

Your uncle is completely confused! His reports show:

- "Desserts cost more than luxury cars?!"
- "We sold 1000 pizzas in one day?!"
- "Free burgers generating millions in revenue?!"
- "100% of payments are in cash?!"

He has NO IDEA what's real anymore! 😂

**Uncle (confused):** "This data makes no sense! I'm giving you back the restaurant! I don't want it anymore!" 🏳️

---

### 🎓 **CONGRATULATIONS!** 🎓

You've completed the SQL Learning Game! You now know:
- ✅ SELECT & WHERE (filter data)
- ✅ ORDER BY & LIMIT (sort and limit results)
- ✅ GROUP BY & Aggregations (calculate totals and averages)
- ✅ JOIN (combine multiple tables)
- ✅ INSERT & UPDATE (modify data)

You're ready to query real databases like a pro! 🚀

**Thanks for playing!** 🎮
        """,
        teaches_concepts=["INSERT", "UPDATE", "SET", "VALUES", "Data modification"]
    )
    
    # Challenge 5.1: Insert fake orders
    level5.add_challenge(Challenge(
        question="**Sabotage 1:** Add 50 fake Pizza orders with price of $0.01 to make Pizza look unprofitable! Use: `INSERT INTO orders (order_id, customer_name, food_item, category, quantity, price, payment_method, order_time) VALUES (...)`\n\n*(Hint: Use order_ids 10001-10050 to avoid conflicts, and any fake values)*",
        expected_result=None,  # No expected result for write queries
        expected_query="INSERT INTO orders VALUES (10001, 'Fake Customer', 'Pizza', 'Main', 1, 0.01, 'Cash', '2025-12-31 23:59:59')",
        hint_1="INSERT INTO orders (order_id, customer_name, food_item, category, quantity, price, payment_method, order_time) VALUES (10001, 'Fake', 'Pizza', 'Main', 1, 0.01, 'Cash', '2025-01-01')",
        hint_2="You need to insert at least one fake order. Use a high order_id like 10001 to avoid conflicts.",
        hint_3="INSERT INTO orders VALUES (10001, 'Sabotage', 'Pizza', 'Main', 100, 0.01, 'Cash', '2025-01-01')",
        allows_write=True
    ))
    
    # Challenge 5.2: Update dessert prices
    level5.add_challenge(Challenge(
        question="**Sabotage 2:** Make all Desserts look ridiculously expensive! Multiply their prices by 100! Use: `UPDATE orders SET price = price * 100 WHERE category = 'Dessert'`",
        expected_result=None,
        expected_query="UPDATE orders SET price = price * 100 WHERE category = 'Dessert'",
        hint_1="Use UPDATE to modify existing rows: UPDATE orders SET price = price * 100 WHERE category = 'Dessert'",
        hint_2="The syntax is: UPDATE table SET column = new_value WHERE condition",
        hint_3="UPDATE orders SET price = price * 100 WHERE category = 'Dessert'",
        allows_write=True
    ))
    
    # Challenge 5.3: Change payment methods
    level5.add_challenge(Challenge(
        question="**Sabotage 3:** Hide the digital audit trail! Change ALL payment methods to 'Cash' so uncle can't track online/card transactions. Use: `UPDATE orders SET payment_method = 'Cash'`",
        expected_result=None,
        expected_query="UPDATE orders SET payment_method = 'Cash'",
        hint_1="UPDATE all rows (no WHERE clause): UPDATE orders SET payment_method = 'Cash'",
        hint_2="Without a WHERE clause, UPDATE affects ALL rows!",
        hint_3="UPDATE orders SET payment_method = 'Cash'",
        allows_write=True
    ))
    
    # Challenge 5.4: Duplicate popular items
    level5.add_challenge(Challenge(
        question="**Sabotage 4:** Make 'Soup' look absurdly popular! Insert duplicate orders by copying all Soup orders with new IDs. Use: `INSERT INTO orders SELECT order_id + 20000, customer_name, food_item, category, quantity, price, payment_method, order_time FROM orders WHERE food_item = 'Soup'`",
        expected_result=None,
        expected_query="INSERT INTO orders SELECT order_id + 20000, customer_name, food_item, category, quantity, price, payment_method, order_time FROM orders WHERE food_item = 'Soup'",
        hint_1="You can INSERT by selecting from the same table! Use INSERT INTO orders SELECT ... FROM orders WHERE food_item = 'Soup'",
        hint_2="Add a large number to order_id to create new IDs: order_id + 20000",
        hint_3="INSERT INTO orders SELECT order_id + 20000, customer_name, food_item, category, quantity, price, payment_method, order_time FROM orders WHERE food_item = 'Soup'",
        allows_write=True
    ))
    
    levels.append(level5)
    
    return levels


# Create and export all levels
ALL_LEVELS = create_all_levels()


def get_level(level_num: int) -> Level:
    """Get a specific level by number."""
    if 1 <= level_num <= len(ALL_LEVELS):
        return ALL_LEVELS[level_num - 1]
    return None


def get_total_levels() -> int:
    """Get total number of levels in the game."""
    return len(ALL_LEVELS)
