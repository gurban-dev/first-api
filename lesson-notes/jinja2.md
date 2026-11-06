Jinja2 is a Python templating engine. It allows you to generate HTML pages dynamically using Python.

### Static HTML vs. Jinja2 Templates

Consider this static HTML:
```html
<h1>Welcome, John!</h1>
```
This is static HTML. Every visitor receives exactly the same content.

Now consider this Jinja2 template:
```html
<h1>Welcome, {{ username }}!</h1>
```
The `{{ username }}` part is a Jinja2 template expression.

### Dynamic Rendering with Python

Python can supply the value dynamically:
```python
return templates.TemplateResponse(
    request=request,    
    name="index.html",    
    context={        
        "username": "John"    
    }
)
```

Jinja2 replaces `{{ username }}` with `John` before returning the HTML page. 

### Final Output

The browser receives the final rendered HTML:
```html
<h1>Welcome, John!</h1>
```