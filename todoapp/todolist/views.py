import logging
from django.shortcuts import render, redirect
from .models import Todo, Category

logger = logging.getLogger(__name__)

# Create your views here.

def index(request): # the index view
    todo_list = Todo.objects.all() # querying all todos with the object manager
    categories = Category.objects.all() # getting all categories with object manager
    current_todo = Todo.objects.filter(completion='todo')
    current_in_progress = Todo.objects.filter(completion='inProgress')
    current_completed = Todo.objects.filter(completion='completed')
    cat_todos = {}
    for cat in categories:
        categorized_todo = Todo.objects.filter(category=cat.id)
        cat_todos[cat.name] = categorized_todo

    for t in todo_list:
        t.dueness_calculator()
        t.save()
        logger.info(t.dueness)

    categorized_todos = cat_todos.items()

    if (request.method == "POST"): # checking if the request method is a POST
        logger.info(request.POST)
        if ("todoAdd" in request.POST): # checking if there is a request to add a todo
            logger.info("todo add being called")
            title = request.POST["description"] # title
            todo_date = str(request.POST["date"]) # date
            category = request.POST["category_select"] # category
            content = title + " -- " + todo_date + " -- " + category # content
            current_todo = Todo(title=title, content=content, due_date=todo_date, category=Category.objects.get(name=category), completion="todo", dueness=0)
            current_todo.save() # saving the todo
            return redirect("/") # reloading the page

        if ("todoDelete" in request.POST): # checking if there is a request to delete a todo
            todo_id = request.POST["todoDelete"]
            current_todo = Todo.objects.get(id=int(todo_id)) # getting todo id
            current_todo.delete() # deleting todo
            return redirect("/") # reloading the page

        if ("editTodo" in request.POST):
            todo_id = request.POST["editTodo"]
            current_todo = Todo.objects.get(id=int(todo_id))
            logger.info(todo_id)
            logger.info(current_todo.title)
            logger.info(current_todo.due_date)
            logger.info(current_todo.category)
            logger.info(current_todo.content)
            current_todo.title = request.POST["edit_description" + todo_id] or current_todo.title
            current_todo.due_date = str(request.POST["edit_due_date" + todo_id]) or str(current_todo.due_date)
            updated_category = request.POST["edit_category_select" + todo_id] or current_todo.category
            current_todo.category = Category.objects.get(name=updated_category)
            current_todo.content = current_todo.title + " -- " + current_todo.due_date + " -- " + str(current_todo.category)
            logger.info(current_todo)
            current_todo.save()
            return redirect("/")

        if ("categoryAdd" in request.POST):
            category_name = request.POST["category"] # category
            current_cat = Category(name=category_name)
            current_cat.save()
            return redirect("/") # reloading the page
        
        if ("categoryDelete" in request.POST): # checking if there is a request to delete a category
            category_id = request.POST["categoryDelete"]
            current_cat = Category.objects.get(id=int(category_id)) # getting category by id
            current_cat.delete() # deleting category
            return redirect("/") # reloading the page

        # TODO: add in backend functionality for switching from todo, inprogress, and complete
        if ("todo" in request.POST or "inProgress" in request.POST or "completed" in request.POST):
            if ("todo" in request.POST):
                logger.info("todo being called")
                todo_id = request.POST["todo"]
                logger.info("todo is in the name")
                current_todo = Todo.objects.get(id=int(todo_id)) # use todo ID to get the todo
                current_todo.completion = "todo"
                current_todo.save()
                return redirect("/") # reloading the page

            if ("inProgress" in request.POST):
                logger.info("in progress add being called")
                todo_id = request.POST["inProgress"]
                logger.info(todo_id)
                current_todo = Todo.objects.get(id=int(todo_id)) # use todo ID to get the todo
                current_todo.completion = "inProgress"
                current_todo.save()
                return redirect("/") # reloading the page

            if ("completed" in request.POST):
                logger.info("completed being called")
                todo_id = request.POST["completed"]
                logger.info("completed is in the name")
                current_todo = Todo.objects.get(id=int(todo_id)) # use todo ID to get the todo
                current_todo.completion = "completed"
                current_todo.save()
                return redirect("/") # reloading the page

    return render(request, "index.html", {"todo_list": todo_list, "categories": categories, "todo": current_todo, "in_progress": current_in_progress, "completed": current_completed, "categorized_todos": categorized_todos})
