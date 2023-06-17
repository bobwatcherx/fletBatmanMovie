from flet import *
from pocketbase import PocketBase
url = 'https://bewildered-author.pockethost.io'
client = PocketBase(url)
import webbrowser

def main(page:Page):
	page.scroll = "auto"
	page.window_width = 400
	# THIS FOR SHOW HIDE CREATE AND COMMENT BUTTON
	showelement = Text("")
	page.padding = 0
	page.spacing = 0
	movierate = Text(1,size=20,weight="bold")

	def submitnewpost(e):
		try:
			res = client.collection("movies_col").create({
			    "poster": newposter.content.controls[0].value,
				 "title": newposter.content.controls[1].value,
			    "year": newposter.content.controls[2].value,
			    "trailer": newposter.content.controls[3].value,
			    "plot": newposter.content.controls[4].value,
			    "genre": newposter.content.controls[5].value,
			    "runtime": newposter.content.controls[6].value,

				})
			page.snack_bar = snack_open
			snack_open.content.value = "success created movie"
			snack_open.content.size = 30
			page.snack_bar.open = True
			newposter.open = False
			getPostMovie.controls.clear()
			page.update()
			post = client.collection("movies_col").get_full_list()
				# print("hasilnya",post)
			for x in post:
				print(x.collection_id['id'])
				getPostMovie.controls.append(
						Column([
						Row([
							Image(src=x.collection_id['poster'],
							fit="cover",
							),
							],alignment="center"),
						Row([
						Text(x.collection_id['title'],weight="bold",
							size=25
							),
						Text(x.collection_id['year'],
							weight="bold"
							)
							],alignment="spaceBetween"),
						Row([
							Container(
								padding=10,
								border_radius=30,
								bgcolor="red200",
								content=Text(x.collection_id['genre'])
								)
							,
							TextButton("Watch Trailer",
								data=x.collection_id['trailer'],
								on_click=openyt
								)
							],alignment="spaceBetween"),
						Row([
							Text(x.collection_id['plot']),
							],alignment="spaceBetween",
							wrap=True
							),
						Row([
							Text(x.collection_id['runtime']),
							
							]),
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
			page.update()
		except Exception as e:
			print(e)
			page.snack_bar = snack_open
			snack_open.content.value = e
			snack_open.content.size = 30
			snack_open.content.bgcolor = "red"
			page.snack_bar.open = True
			page.update()
		page.update()


	newposter = AlertDialog(
		title=Text("new Poster"),
		content=Column([
			TextField(label="poster"),
			TextField(label="title"),
			TextField(label="year"),
			TextField(label="trailer url video"),
			TextField(label="plot"),
			TextField(label="genre"),
			TextField(label="runtime"),

			],alignment="center"),
		actions=[
		ElevatedButton("Create New",
			bgcolor="blue",
			on_click=submitnewpost
			)
		],
		actions_alignment="center"
		)

	def createnewposter(e):
		page.dialog = newposter
		newposter.open = True
		page.update()


	page.floating_action_button  = FloatingActionButton(
		icon="add",
		bgcolor="blue",
		on_click=createnewposter,
		visible=False  
		)

	movieId  = Text("")
	is_login = False
	snack_open = SnackBar(
		content=Text(""),
		)
	getPostMovie = Column()



	def registeruser(e):
		print("!!!!!!!!!!!!!!!!!!!!!")
		print(dialogcreateuser.content.controls[5].value)
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
				"is_admin":dialogcreateuser.content.controls[5].value
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
			page.snack_bar = SnackBar(
				Text(e,color="white",size=20),
				bgcolor="red"
				)
			page.snack_bar.open = True
			page.update()
	def removecomment(e):
		delid = e.control.data['id']
		print("))))))))))")
		print(delid)
		print("dd",movieId.value)

		try:
			deletefun = client.collection("comments_col").delete(delid)
			mycomment.content.controls.clear()
			page.update()
			comm = client.collection("comments_col").get_full_list()
			filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == movieId.value, comm))
			checkIsUser = client.auth_store.model.collection_id['username']


			print(filtered_comm)
			for b in filtered_comm:
				mycomment.content.controls.append(
				ListTile(
					leading=Icon(name="account_circle"),
					title=Row([
						Text(b.collection_id['user_name'],weight="bold"),
						Text(f"{b.collection_id['ratting']} likes",size=15,color="green",
							weight="bold"
							),
						],alignment="spaceBetween"),
					subtitle=Row([
						Text(b.collection_id['comments'],
						size=15,
						),
						IconButton(icon="delete",icon_color="red",
							data=b.collection_id,
							on_click=removecomment,
							visible=True if checkIsUser == b.collection_id['user_name'] else False
							)
						],alignment="spaceBetween",wrap=True)

					)
				)
			page.update()
		except Exception as e:
			print(e)
		page.update()

	def sendcomment(e):
		print("movie id ",movieId.value)
		
		print(mylogin.controls[1].value)
		try:
			msg = client.collection("comments_col").create({
			"user_id":client.auth_store.model.collection_id['id'],
			"movie_id":movieId.value,
			"user_name":mylogin.controls[1].value,
			"comments":mycomment.actions[0].controls[0].value,
			"ratting":int(movierate.value)
			})
			mycomment.content.controls.clear()
			comm = client.collection("comments_col").get_full_list()
			filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == movieId.value, comm))
			
			checkIsUser = client.auth_store.model.collection_id['username']
			

			for b in filtered_comm:
				mycomment.content.controls.append(
				ListTile(
				leading=Icon(name="account_circle"),
				title=Row([
					Text(b.collection_id['user_name'],weight="bold"),
					Text(f"{b.collection_id['ratting']} likes",size=15,color="green",
						weight="bold"
						),
					],alignment="spaceBetween"),
				subtitle=Row([
					Text(b.collection_id['comments'],
					size=15,
					),
					IconButton(icon="delete",icon_color="red",
						data=b.collection_id,
						on_click=removecomment,
						visible=True if checkIsUser == b.collection_id['user_name'] else  False
						
						)
					],alignment="spaceBetween",wrap=True)

				)
				)
			mycomment.actions[0].controls[0].value = ""
			movierate.value = 1
			mycomment.actions[1].controls[1].value= 1
			page.update()
		except Exception as e:
			print(e)


	def changeratemovie(e):
		movierate.value = int(e.control.value)
		page.update()

	mycomment = AlertDialog(
		title=Text("Comments"),
		content=Column(alignment="start",scroll="auto"),
		actions=[
		Row([
			TextField(label="insert comment",
				width=170,
				),
			IconButton("send",
				on_click=sendcomment,
				),
			],scroll = "auto"),
		Column([
			Row([
			movierate,
			Icon(name="thumb_up",size=25)
				],alignment="center"),
			Slider(min=1,max=5,value=movierate.value,
				on_change=changeratemovie,
				active_color="red"
				)
			])
		]
		)
	def closedialogregister(e):
		dialogcreateuser.open = False
		page.update()

	def changetoadmin(e):
		dialogcreateuser.content.controls[6].value = "You create Administrator" if dialogcreateuser.content.controls[5].value == True else "You Create user Only"
		dialogcreateuser.content.controls[6].color = "red" if dialogcreateuser.content.controls[5].value == True else "green"
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
			Switch(label="Create Admin",value=False,
				on_change=changetoadmin,
				active_color="red"
				),
			Text("You Create user Only",size=25,
				color="green",weight="bold"
				)

			]),
		actions=[
		ElevatedButton("Close",
			bgcolor="red",
			color="white",
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
		checkIsUser = client.auth_store.model.collection_id['username']


		print(filtered_comm)
		for b in filtered_comm:
			mycomment.content.controls.append(
			ListTile(
				leading=Icon(name="account_circle"),
				title=Row([
					Text(b.collection_id['user_name'],weight="bold"),
					Text(f"{b.collection_id['ratting']} likes",size=15,color="green",
						weight="bold"
						),
					],alignment="spaceBetween"),
				subtitle=Row([
					Text(b.collection_id['comments'],
					size=15,
					),
					IconButton(icon="delete",icon_color="red",
						data=b.collection_id,
						on_click=removecomment,
						visible=True if checkIsUser == b.collection_id['user_name'] else False
						)
					],alignment="spaceBetween",wrap=True)

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
			"photo":mycast.actions[0].controls[2].value,
			"persons":mycast.actions[0].controls[0].value,
			"role":mycast.actions[0].controls[1].value
			})
			mycast.content.controls.clear()
			comm = client.collection("casts_col").get_full_list()
			filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == movieId.value, comm))
			for b in filtered_comm:
				mycast.content.controls.append(
				ListTile(
					leading=Image(src=b.collection_id['photo']),
					title=Column([
						Text(b.collection_id['persons']),
						Text(b.collection_id['role']),

						])
					)
				)
			mycast.actions[0].controls[0].value = ""
			mycast.actions[0].controls[1].value = ""
			mycast.actions[0].controls[2].value = ""
			page.update()
		except Exception as e:
			print(e)

	mycast = AlertDialog(
		title=Text("Casts",weight="bold",size=25),
		content=Column(scroll="auto"),
		actions=[
			Column([
				TextField(label="add person"),
				TextField(label="add role"),
				TextField(label="Photo URL"),
				ElevatedButton("submit",
				on_click=addcastmodel
				),
				],scroll="auto")
		],
		actions_alignment="end"
		)
	mycastdisable = AlertDialog(
		title=Text("Casts",weight="bold",size=25),
		content=Column(scroll="auto"),
		actions=[
			Column([
				Text("You cannot comment here",
					color="red",size=20
					)
				],scroll="auto")
		],
		actions_alignment="end"
		)
	def dialogcastdisable(e):
		page.dialog = mycastdisable
		movieId.value = e.control.data
		mycastdisable.open = True
		mycastdisable.content.controls.clear()
		comm = client.collection("casts_col").get_full_list()
		filtered_comm = list(filter(lambda x: x.collection_id['movie_id'] == e.control.data, comm))

		for b in filtered_comm:
			mycastdisable.content.controls.append(
			ListTile(
				leading=Image(src=b.collection_id['photo']),
				title=Column([
					Text(b.collection_id['persons']),
					Text(b.collection_id['role']),

					])
				)
			)
		print(filtered_comm)
		print("id",e.control.data)
		page.update()

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
				leading=Image(src=b.collection_id['photo']),
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
			# print(client.auth_store.model.collection_id['id'])
			# print()
			# print(loginnow.token)
			page.session.set("keylogin",loginnow.token)
			is_login = True
			content_user.content.content = mycontent
			page.floating_action_button.visible = True

			page.snack_bar = snack_open
			page.snack_bar.open = True
			snack_open.content.size = 30
			snack_open.content.value = "success Login"
			snack_open.bgcolor = "green"

			# LOAD DATA
			if not loginnow.token  == None:
				checkisadmin = client.collection("users_col").get_full_list()
				print("check admin ===========================")
				print(checkisadmin)
				is_admin = False  # Tambahkan variabel is_admin untuk menandai status admin
				for record in checkisadmin:
					if record.collection_id['username'] == mylogin.controls[1].value:
						if record.collection_id['is_admin'] == "true":
							is_admin = True
						break

				if is_admin:
					showelement.value = "isTrue"
					page.floating_action_button.visible = True
					page.controls[0].content.value = "You Admin"
					page.controls[0].bgcolor = "red"
					page.update()
				else:
					showelement.value = "isFalse"
					page.floating_action_button.visible = False
					page.controls[0].content.value = "pocket crud"
					page.controls[0].bgcolor = "blue"
					print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
					print(client.auth_store.model.collection_id)
					page.update()

				print(showelement.value)

				comm = client.collection("casts_col").get_full_list()
				post = client.collection("movies_col").get_full_list()
				for x in post:
					print(x.collection_id['id'])
					getPostMovie.controls.append(
							Column([
							Row([
								Image(src=x.collection_id['poster'],
								height=250,
								fit="cover",
								),
								],alignment="center"),
							Row([
							Text(x.collection_id['title'],weight="bold",
								size=25
								),
							Text(x.collection_id['year'],
								weight="bold"
								)
								],alignment="spaceBetween"),
							Row([
								Container(
									padding=10,
									border_radius=30,
									bgcolor="red200",
									content=Text(x.collection_id['genre'])
									)
								,
								TextButton("Watch Trailer",
									data=x.collection_id['trailer'],
									on_click=openyt
									)
								],alignment="spaceBetween"),
							Row([
								Text(x.collection_id['plot']),
								Container(
									padding=10,
									bgcolor="purple200",
									border_radius=30,
									content=Row([
										Icon(name="timer"),
										Text(x.collection_id['runtime'])
										])
									),
								],alignment="spaceBetween",
								wrap=True
								),
							# BUAT TAMBAH DATA KE MOVIE

							Row([
								IconButton("create",
								icon_color="purple",
								data=x.collection_id['id'],
								on_click=dialogcast,
								visible=False if showelement.value == "isFalse" else True
									),
								IconButton("comment",
								icon_color="red",
								data=x.collection_id['id'],
								on_click=dialogcomment,
								visible=False if showelement.value == "isFalse" else True
								
									)
								],alignment="end"),
							# INI BUAT LIHAT DATA 
							Row([
								TextButton("casts",
								data=x.collection_id['id'],
								on_click=dialogcastdisable,
								visible=True if showelement.value == "isFalse" else False
									),
								TextButton("comment",
								data=x.collection_id['id'],
								on_click=dialogcomment,
								visible=True if showelement.value == "isFalse" else False
								
									)
								]),
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
		showelement.value = ""
		getPostMovie.controls.clear()
		page.floating_action_button.visible = False
		print("logout !!!")
		print(showelement.value)
		page.controls[0].content.value = "pocket crud"
		page.controls[0].bgcolor = "blue"
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
				margin=margin.only(bottom=50,top=20,left=20,right=20),
				content=Container(
					width=page.window_width,
					padding=10,
					bgcolor="white" if is_login == True else "yellow",
					content=mycontent if is_login == True else mylogin
					)
				)
	
	page.add(
		Container(
			width=page.window_width,
			height=70,
			padding=10,
			content=Text("Pocket Crud",color="white",
				weight="bold",
				size=25
				),
			bgcolor="blue",
			),
		Column([
			content_user
			])
		)

flet.app(target=main)
