from flask import Flask, render_template, request, redirect, session
from neo4j import GraphDatabase
import requests
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import string
import socket
from pyaiml21 import Kernel
from glob import glob
from pyswip import Prolog
import openai
import webbrowser
import googlesearch
# Create a Neo4j driver instance
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password")) #insert your neo4j password
logindone = False
name_for_subnet = ''
check_test = None
get_name_database = ''
name_of_frined = ''
response_name = ''
getname = ''
name_of_user = ''
realtionship = ''
tester = ''

def get_completion(query):
     openai.api_key = 'pk-******************************************' #insert your api key
     openai.api_base = 'https://api.pawan.krd/v1'

     response = openai.Completion.create(
         model="text-davinci-003",
         prompt="Human: " + query + "\nAI:",
         temperature=0.7,
         max_tokens=256,
         top_p=1,
         frequency_penalty=0,
         presence_penalty=0,
         stop=["Human: ", "AI: "]
     )

     return response.choices[0].text.strip()
 
def callback(url):
    webbrowser.open(url)

def search_query(query):
    s = googlesearch.search(query, tld="co.in", num=10, stop=1, pause=2)
    for j in s:
        callback(j)

    
def get_name(message):
    nltk_results = ne_chunk(pos_tag(word_tokenize(message)))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                name += nltk_result_leaf[0] + ' '
            return name
        

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_subnet_address():
    str1 = get_ip_address()
    str2 = ''
    i = 0
    for x in range(len(str1)):
        if str1[x] == '.':
            str2 += str1[x]
            i += 1
        elif i == 3:
            break
        else:
            str2 += str1[x]
    return str2

def database(tx, username, password):
    query = f"MATCH (User) WHERE User.username = '{username}' AND User.password = '{password}' RETURN true"
    result = tx.run(query)
    record = result.single()
    if record:
        return record[0]
    else:
        return False

def check(username, password):
    with driver.session() as session:
        return session.read_transaction(database, username, password)
    
def get_ip_user(tx, username):
    query = f"MATCH (User) WHERE User.username = '{username}' RETURN User.subnet"
    result = tx.run(query)
    record = result.single()
    if record:
        return record[0]
    else:
        return False

def check_ip_user(username):
    with driver.session() as session:
        return session.read_transaction(get_ip_user, username)
    
def get_username_second(tx, username,ip):
    global get_name_database
    query = f"MATCH (User) WHERE User.username <> '{username}' and User.subnet = '{ip}' RETURN User.username"
    result = tx.run(query)
    record = result.single()
    if record:
        get_name_database = record[0]
        return record[0]
    else:
        return False

def check_username_second(username,ip):
    with driver.session() as session:
        return session.read_transaction(get_username_second, username,ip)
    
def check_if_equal(username):
    ip_returns = check_ip_user(username)
    username2 = check_username_second(username,ip_returns)
    ip_returns2 = check_ip_user(username2)

    if ip_returns == ip_returns2:
        return "Yes"
    else:
        return "No"
    
def update_ip(tx,username):
    new_ip = get_subnet_address()
    query = f"MATCH (User) WHERE User.username = '{username}' SET User.subnet = '{new_ip}'"
    result = tx.run(query)
    record = result.single()
    if record:
        return record[0]
    else:
        return False

def run_update_ip(name):
    with driver.session() as session:
        return session.write_transaction(update_ip, name)
    
def extract_relationship(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    relationship = None

    for word, tag in tagged:
        if tag == 'NN' and word.lower() == 'friend':
            relationship = word
        elif tag == 'NN' and word.lower() == 'brother':
            relationship = word
        elif tag == 'NN' and word.lower() == 'sister':
            relationship = word
        elif tag == 'NN' and word.lower() == 'father':
            relationship = word
        elif tag == 'NN' and word.lower() == 'mother':
            relationship = word
        elif tag == 'NN' and word.lower() == 'uncle':
            relationship = word
        elif tag == 'NN' and word.lower() == 'aunt':
            relationship = word
        elif tag == 'NN' and word.lower() == 'dont know':
            relationship = "dont know"

    return relationship

def create_social_network(tx, username, friend_name, relationship):
    username = username.replace(" ", "")
    friend_name = friend_name.replace(" ", "")
    query = """
    MATCH (a:User {username: $username}), (b:User {username: $friend_name})
    CREATE (a)-[r:`{relationship}`]->(b)
    RETURN r
    """
    query = query.replace("{relationship}", relationship)  # Replace {relationship} with the actual value
    result = tx.run(query, username=username, friend_name=friend_name)
    record = result.single()
    return record['r'] if record else None


def check_social_network(username, friend_name, relationship):
    with driver.session() as session:
        return session.write_transaction(create_social_network, username, friend_name, relationship)

def nltk_check_function(message):
    messageToReturn = ''
    if '-' in message or '+' in message:
        messageToReturn = message
    else:
        message = message.lower()
        message = message.translate(str.maketrans("", "", string.punctuation))
        tokenizer = nltk.sent_tokenize(message)
        corrected_tokenizer = []
        for sentence in tokenizer:
            words = nltk.word_tokenize(sentence)
            corrected_words = [w for w in words]
            corrected_sentence = " ".join(corrected_words)
            corrected_tokenizer.append(corrected_sentence)
        autocorrected_message = " ".join(corrected_tokenizer)
        messageToReturn = autocorrected_message
    return messageToReturn
    
def get_name2():
    global name_of_user
    name_of_user = name_of_user.capitalize()
    response = k.respond("what is my name", "Ali")
    if "unknown" in response:
        response = response.replace("unknown",name_of_user)
        return get_name(response).lower()
    else:
        return get_name(response).lower()
     
def save_relationship(person1, person2, relationship):
    prolog.assertz(f"relationship({person1}, {person2}, {relationship})")

def write_relationships_to_file(file_path):
    with open(file_path, "a") as file:
        query = "relationship(X, Y, Z)"
        results = list(prolog.query(query))
        for result in results:
            file.write(f"{result['X']}, {result['Y']}, {result['Z']}.\n")

def remove_duplicates(file_path):
    # Read the file and store unique relationships in a set
    relationships = set()
    with open(file_path, "r") as file:
        for line in file:
            relationships.add(line.strip())

    # Write the unique relationships back to the file
    with open(file_path, "w") as file:
        for relationship in relationships:
            file.write(relationship + "\n")
            
def create_siblings(name):
    name = name.replace(" ", "")
    with driver.session() as session:
        session.run(
            "CREATE (u:User {username: $name})",
            name=name
        )

    
# Initialize the Prolog engine
prolog = Prolog()

# Load the existing Prolog file or create a new one
prolog.consult("relationships.pl")

app = Flask(__name__)
app.secret_key = 'esjokeryt'  # Set a secret key for session management

k = Kernel()
aiml_files = glob("AIML_FILES/*.aiml")
for file_path in aiml_files:
    k.learn_aiml(file_path)
k.learn(r'D:\BOT\Easy-Chatbot-master\AIML_FILES\test.aiml')

@app.route("/")
def home():
    if logindone == True:
        return render_template("index.html")
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    global logindone
    global name_for_subnet
    global check_test
    global name_of_user
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        username = str(username)
        password = str(password)
        name_of_user = username
        name_for_subnet = username
        output = check(username, password)
        if output:
            session['success_message'] = "Login successful!"
            logindone = True
            check_test = check_if_equal(name_for_subnet)
            run_update_ip(name_of_user)
            
            return redirect("/")
        else:
            session['error_message'] = "Invalid username or password"
            return redirect("/login")

    error_message = session.pop('error_message', None)
    success_message = session.pop('success_message', None)
    return render_template("login.html", error=error_message, success=success_message)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        subnet_address = get_subnet_address()
        with driver.session() as session:
            session.run(
                "CREATE (u:User {username: $username, password: $password, subnet: $subnet_address})",
                username=username,
                password=password,
                subnet_address=subnet_address
            )

        message = "Account created successfully!"
        return render_template("signup.html", message=message)

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/login")

@app.route("/get", methods=["GET", "POST"])
def get_bot_response():
    global get_name_database
    global getname
    global realtionship
    global tester
    global name_of_user
    name_of_user = get_name2()
    user_name = ''
    counter = session.get('counter', 0)
    query = request.args.get('msg')
    realtionship = extract_relationship(query)
    response = ''
    test_response = k.respond(query, "Ali")
    query = query.replace('?','')
    query = query.replace('.','')
    if check_test == "Yes" and counter == 3 :
            response = f"Hey, did you know who is {get_name_database}?"
            tester = response
    else:
            query = query.capitalize()
            if "is my friend" in query or "is my sister" in query or "is my brother" in query or "is my mother" in query or "is my father" in query:
                if "yes" in query or "Yes" in query:
                    name2 = get_name_database
                else:
                    name2 = str(get_name(query).lower())
                realtionship = extract_relationship(query)
                save_relationship(name2,name_of_user,realtionship)
                write_relationships_to_file("relationships.pl")
                if "yes" in query or "Yes" in query:
                    pass
                else:
                    create_siblings(name2)
                check_social_network(name2,name_of_user,realtionship)
            query = query.lower()
            if any(keyword in query for keyword in ["write", "search", "fix", "tell"]):
                response = get_completion(query)
            elif "play" in query or "image" in query or "video" in query or "images" in query:
                search_query(query)
                response = "Ok wait"
            elif "Hey, did you know who is" in tester:
                getname = get_name2()
            if any(keyword in query for keyword in ["my ip", "ip", "what is my ip", "tell my ip"]):
                response = get_ip_address()
            elif any(keyword in query for keyword in ["what is your name", "your name", "yours name", "your's name"]):
                response = "My name is ELEVEN"
            else:
                text = str(query).lower()
                response = k.respond(query, "Ali")
                if response == "i was created by unknown" or "i was created by unknown" in response:
                    response = "I was made by a handsome person named ALI."
                elif response == "unknown":
                    if '+' in query or '-' in query or '/' in query or '*' in query:
                        response = get_completion(query)
                    else:
                        if "play" in query or "image" in query or "video" in query or "images" in query:
                            result = "ok wait"
                        else: 
                            result = get_completion(query)
                        result = nltk_check_function(result)
                        aiml_data = f'<category><pattern>{query}</pattern><template>{result}</template></category>'
                        aiml_file_path = r"D:\BOT\Easy-Chatbot-master\AIML_FILES\test.aiml"
        
                        with open(aiml_file_path, 'r') as file:
                            content = file.readlines()
            
                        index = -1
                        for i, line in enumerate(content):
                            if "<aiml>" in line:
                                index = i
                                break
        
                        if index != -1:
                            if aiml_data not in content:
                                if not content[-1].endswith('\n'):
                                    aiml_data = '\n' + aiml_data
                                content.insert(index + 1, aiml_data + "\n")
                        else:
                            if aiml_data not in content:
                                content.insert(index + 1, '<aiml>\n')
                                content.insert(index + 2, aiml_data + '\n')
                                content.insert(index + 3, '</aiml>\n')

                        with open(aiml_file_path, 'w') as file:
                            file.writelines(content)

                        aiml_files = glob("AIML_FILES/*.aiml")
                        for file_path in aiml_files:
                            k.learn_aiml(file_path)

                        response = k.respond(query, "Ali")
                elif "unknown" in response:
                    response = response.replace("unknown", name_of_user)
                elif text.startswith("name"):
                    response = "Who's name? Are you asking about your name?"
        
    
    if response:
        counter += 1
        session['counter'] = counter
        remove_duplicates("relationships.pl")
        return response
    else:
        return ":)"
    


if __name__ == "__main__":
    
    app.run(port='8888')
