# Drops

> _... is a lightweight message-broker purely written in Python 3.12, useful for developing large-scale event-based systems._


Some benefits from using event based architectures:  

* **Decoupling**: Events decouple components by allowing them to interact without needing to know the details of each other's implementations.
* **Scalability**: Event-based architectures can scale more easily since components can be added or removed without disrupting the entire
  system.
* **Flexibility**: Events provide flexibility by allowing components to react to changes or triggers asynchronously, enabling dynamic behavior.
* **Loose Coupling**: Event-based systems promote loose coupling between components, reducing dependencies and making the system more
  maintainable and adaptable.

!!! warning
    Since drops is under heavy development, the API is probably going to change
    heavily until version 1.0 is reached


---


## Minimal Example

Create a python file called `hello.py` with the following code:

```python title="hello.py" 
{!../docs_src/hello.py!}
```

And then run your application from your terminal


<!-- termynal -->

```
> python3 hello.py
Hello Alice
Goodbye Alice
```