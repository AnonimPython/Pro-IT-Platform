import reflex as rx

config = rx.Config(
    app_name="Pro_IT_Platform",
    frontend_port=3000,
    #! FOR TEST 
    db_url="sqlite:///pro-it.db",
    #! IN REALIZE UNCOMMEMT THIS
    # db_url="postgresql://user:password@localhost:5432/pro-it.db",
)