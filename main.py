from flet import *
from pocketbase import PocketBase
url = 'https://bewildered-author.pockethost.io'
client = PocketBase(url)
import webbrowser

def main(page:Page):
	page.scroll = "auto"
	page.window_width = 400
	movieId  = Text("")
	is_login = False
	snack_open = SnackBar(
		content=Text(""),
		)
	getPostMovie = Column()
	def registeruser(e):
		try:
			adduser = client.collection("users").create(body_params={
				"username":dialogcreateuser.content.controls[0].value,
				"password":dialogcreateuser.content.controls[4].value,
				"email":dialogcreateuser.content.controls[2].value,
				"name":dialogcreateuser.content.controls[3].value,
				"passwordConfirm":dialogcreateuser.content.controls[4].value,

			})
			res = client.collection("users_col").create(
			{
				"username":dialogcreateuser.content.controls[0].value,
				"address":dialogcreateuser.content.controls[1].value,
				"email":dialogcreateuser.content.controls[2].value,
				"name":dialogcreateuser.content.controls[3].value,
				"password":dialogcreateuser.content.controls[4].value,
			}
			)
			page.snack_bar = snack_open
			snack_open.content.value = "success created user"
			snack_open.content.size = 30
			page.snack_bar.open = True
			dialogcreateuser.open = False
			dialogcreateuser.content.controls[0].value = ""
			dialogcreateuser.content.controls[1].value = ""
			dialogcreateuser.content.controls[2].value = ""
			dialogcreateuser.content.controls[3].value = ""
			dialogcreateuser.content.controls[4].value = ""
			mylogin.controls[1].value = dialogcreateuser.content.controls[0].value
			page.update()
		except Exception as e:
			print(e)

	def sendcomment(e):
		print("movie id ",movieId.value)
		try:
			msg = client.collection("comments_col").create({
			"user_id":client.auth_store.model.collection_id['id'],
			"movie_id":movieId.value,
			"comments":mycomment.actions[0].controls[0].value
			})
			mycomment.content.controls.clear()
			comm = client.collection("comments_col").get_full_list()
			filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == movieId.value, comm))
			for b in filtered_comm:
				mycomment.content.controls.append(
				ListTile(
					leading=Icon(name="account_circle"),

					title=Text(b.collection_id['comments'])
					)
				)
			mycomment.actions[0].controls[0].value = ""
			page.update()
		except Exception as e:
			print(e)


	mycomment = AlertDialog(
		title=Text("Comments"),
		content=Column(alignment="start"),
		actions=[
		Column([
			TextField(label="insert comment",
				width=200
				),
			IconButton("send",
				on_click=sendcomment
				)
			])
		]
		)
	def closedialogregister(e):
		dialogcreateuser.open = False
		page.update()

	dialogcreateuser = AlertDialog(
		modal=True,
		title=Text("create User"),
		content=Column([
			TextField(label="create username"),
			TextField(label="address"),
			TextField(label="email"),
			TextField(label="name"),
			TextField(label="create password",
				password=True,
				can_reveal_password=True
				),
			]),
		actions=[
		ElevatedButton("Close",
			bgcolor="red",
				on_click=closedialogregister
				),
			ElevatedButton("create new",
				on_click=registeruser
				),

		],
		actions_alignment="spaceBetween"
		)
	def dialogcomment(e):
		page.dialog = mycomment
		movieId.value = e.control.data
		mycomment.open = True
		mycomment.content.controls.clear()
		comm = client.collection("comments_col").get_full_list()
		filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == e.control.data, comm))

		for b in filtered_comm:
			mycomment.content.controls.append(
			ListTile(
				leading=Icon(name="account_circle"),
				title=Text(b.collection_id['comments'])
				)
			)
		print(filtered_comm)
		print("tolol")

		print("id",e.control.data)
		page.update()
	def addcastmodel(e):
		print("movie id ",movieId.value)
		try:
			msg = client.collection("casts_col").create({
			"movie_id":movieId.value,
			"persons":mycast.actions[0].controls[0].value,
			"role":mycast.actions[0].controls[1].value
			})
			mycast.content.controls.clear()
			comm = client.collection("casts_col").get_full_list()
			filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == movieId.value, comm))
			for b in filtered_comm:
				mycast.content.controls.append(
				ListTile(
					leading=Icon(name="account_circle"),
					title=Column([
						Text(b.collection_id['persons']),
						Text(b.collection_id['role']),

						])
					)
				)
			mycast.actions[0].controls[0].value = ""
			mycast.actions[0].controls[1].value = ""
			page.update()
		except Exception as e:
			print(e)

	mycast = AlertDialog(
		content=Column(),
		actions=[
			Column([
				TextField(label="add person"),
				TextField(label="add role"),
				ElevatedButton("submit",
				on_click=addcastmodel
				),
				])
		],
		actions_alignment="end"
		)
	def dialogcast(e):
		page.dialog = mycast
		movieId.value = e.control.data
		mycast.open = True
		mycast.content.controls.clear()
		comm = client.collection("casts_col").get_full_list()
		filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == e.control.data, comm))

		for b in filtered_comm:
			mycast.content.controls.append(
			ListTile(
				leading=Icon(name="account_circle"),
				title=Column([
					Text(b.collection_id['persons']),
					Text(b.collection_id['role']),

					])
				)
			)
		print(filtered_comm)
		print("id",e.control.data)
		page.update()
	def openyt(e):
		webbrowser.open(e.control.data)
		page.update()
		
	def loginuser(e):
		try:
			loginnow = client.collection("users").auth_with_password(
			mylogin.controls[1].value,mylogin.controls[2].value
			)
			# print(dir(client.auth_store.model))
			print(client.auth_store.model.collection_id['id'])
			# print()
			# print(loginnow.token)
			page.session.set("keylogin",loginnow.token)
			is_login = True
			content_user.content.content = mycontent
			page.snack_bar = snack_open
			page.snack_bar.open = True
			snack_open.content.size = 30
			snack_open.content.value = "success Login"
			snack_open.bgcolor = "green"

			# LOAD DATA
			if not loginnow.token  == None:
				
				post = client.collection("movies_col").get_full_list()
				# print("hasilnya",post)
				for x in post:
					print(x.collection_id['id'])
					getPostMovie.controls.append(
						Column([
						Image(src=x.collection_id['poster'],
							height=250,
							fit="cover",
							),
						Row([
						Text(x.collection_id['title'],weight="bold",
							size=25
							),
						Text(x.collection_id['year'],
							weight="bold"
							)
							],alignment="spaceBetween"),
						Row([
							Text(x.collection_id['genre']),
							TextButton("Watch Trailer",
								data=x.collection_id['trailer'],
								on_click=openyt
								)
							],alignment="spaceBetween"),
						Row([
							Text(x.collection_id['plot']),
							Text(x.collection_id['runtime']),
							],alignment="spaceBetween"),
						Row([
							IconButton("create",
							icon_color="purple",
							data=x.collection_id['id'],
							on_click=dialogcast
								),
							IconButton("comment",
							icon_color="red",
							data=x.collection_id['id'],
							on_click=dialogcomment
								)
							],alignment="end"),
						Divider()
							])
						)
			else:
				print("Data not found")
		except Exception as e:
			page.snack_bar = snack_open
			snack_open.open = True
			page.snack_bar.open = True
			snack_open.content.size = 30
			snack_open.content.value = e
			snack_open.bgcolor = "red"
		page.update()

	def createAccount(e):
		page.dialog = dialogcreateuser
		dialogcreateuser.open = True
		page.update()


	mylogin = Column([
		Text("Login User",size=20,weight="bold"),
		TextField(label="Username"),
		TextField(label="Password",
			password=True,
				can_reveal_password=True
				),
		ElevatedButton("Login Now",
			bgcolor="green",color="white",
			on_click=loginuser
			),
		Row([
			TextButton("Create Account",
				on_click=createAccount
				)
			],alignment="end")
		])
	def logoutnow(e):
		page.session.remove("keylogin")
		mylogin.controls[1].value = ""
		mylogin.controls[2].value = ""
		content_user.content.content = mylogin
		page.snack_bar = snack_open
		page.snack_bar.open = True
		snack_open.content.size = 30
		snack_open.content.value = "Logout now"
		snack_open.bgcolor = "red"
		page.update()

	mycontent = Column([
		Row([
		Text("Welcome Back",weight="bold"),
		TextButton("logout",on_click=logoutnow)
		],alignment="spaceBetween"),
		getPostMovie
		],alignment="center")

	content_user = Card(
				elevation=10,
				content=Container(
					width=page.window_width,
					padding=10,
					bgcolor="white" if is_login == True else "yellow",
					content=mycontent if is_login == True else mylogin
					)
				)

	page.add(
		AppBar(
			title=Text("Pocket Crud",color="white",
				weight="bold"
				),
			bgcolor="blue",
			),
		Column([
			content_user
			])
		)

flet.app(target=main)
