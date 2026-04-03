# Understanding Requirement: tasks explanations 
**no LLM assistance**

## Main App

The root the project is the main app that act as the main page and navigation to the diffrent tasks' pages. Every task has a deteacated page and a folder with the code and data.
`streamlit` is capable of to multi page apps which make it easier to present all the task in one app.

`streamlit` was chosen as it was recommended by the course lecturer, has good tutorials in YouTube and good integration with `Pandas` and visualisation tools. For addition `streamlit` have there own cloud for deployment. 

### Technologies and Libraries (all tasks)
The app use `sqlite3` and `pandas` to access the data and data manipulation.
The libraries was chosen because was simple to and good integration between them and with `streamlit`.
`sqlite3` is a powerful and popular SQL package that doesn`t require serveres.
`pandas` it's a great tool for data maniulation, has very good documentation, good Python integration, SQL integration, good with the expected size of data.




## Tasks 1

### What was Built
Task 1 is a baby named explorer App. It can help to see insights about the patterns of baby name in the US and visualise the data in a meaningful ways.

### Technologies and Libraries
`sqlite3` and `pandas` (see the Main App - Technologies and Libraries (all tasks))

### Challenges and Solutions
I am not used for front end development So making an app was a challenge for me. A solution was a lot of YouTube tutorials and therelative simplicity of `streamlit`.
Though the code itself was written with the help of copilot CLI, I wanted to understand the code which was the challenge because I didn't know SQL before this course. I use documentation, Youtube tutorials and ChatGPT in order to understand the different parts of the code. 




## Tasks 2

### What was Built
Task 2 is a Oscar Actor explorer. the main idea is to use ORM (Object Relational Mapping) in order to interact with the database instead of raw SQL queries. The app calculate and presents statistics abput actors and enrich  them with Wikipedia API. In addition the app presents interesting finds and did you know? section.


### Technologies and Libraries
`sqlite3` and `pandas` (see the Main App - Technologies and Libraries (all tasks))
`pony.orm` was used as an ORM tool. I chose because of the good documentation and Python integration. in addition I really liked the name of the package.


### Challenges and Solutions
I had a problem automatically creating and validate that the database is OK. The solution was to a function that cheak the databse in runtime, what was later formulate to the utiles file.
I had a problem to understand the discover pattern section and "translate" the pattern to SQL queries. The solution was mostly to get help from copilot and fixing it when needed.




## Tasks 3

### What was Built
Task 3 is a Pokémon battle arena. The app load data of diffrent Pokémons such as name, type and power. Then it enable the players to each choose 1-3 pokémon. Run turn-based battel until a one player win. It also enable cheat codes and Pokémon Analysis.


### Technologies and Libraries
`sqlite3` and `pandas` (see the Main App - Technologies and Libraries (all tasks))


### Challenges and Solutions
This was the hardest task for me. Task 3 was more complicated than task 1 and task 2 as it required copliceted battle engine. The solution was to work with different files and function and to try until it worked.
One main challenge was a SQL database lock that was because different functions try to connect to the same database in the same time. The solution was to review carefully each function and make sure that it's doenst calls to other functions that also try to connect to the database before this function close the databse connaction.


## Tasks 4

### What was Built
A game that SQL queries. The game is a restaurant and the player as the restaurant's owner tried to see insights about the orders. the player used different SQL queries to different relevant data such as Most popular category are the food that was bought the most.


### Technologies/libraries
`sqlite3` and `pandas` (see the Main App - Technologies and Libraries (all tasks))


### Challenges and Solutions
The challenge was mostly thinking about the idea that was in one hand simple enough to build as assignment and in other hand also interesting.
Other challenge was to understand the game logic and make sure it understandable easily to the players.
Both challenges was solved via thinking and looking on the app and try to think as a player.


