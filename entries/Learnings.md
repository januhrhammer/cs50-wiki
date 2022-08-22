# Learnings

  
My learnings from finishing the 2nd problem set of the cs50w course, adding functionality to a [Django](/wiki/Django) wiki project.

# Django  

**render()**  

- renders a template
- usage: render(request, "url", {"context": context})
- context can be a variable or a form that gets accessible in html templates

**HttpResponseRedirect()**

- redirects to the url passed
- usage: HttpResponseRedirect("url")


**reverse()**

- returns the url of a specific url pattern
- usage: reverse("urlpattern", args=None, Kwargs=None)
- args as [argument] or kwargs as {"argument": argument}

