# Learn by example

In this section we will focus on a standard use-case of using Drops in the context of discrete-event simulations. The following example will
also play another role in the advanced section where we will describe how to combine Drops with Flask to make a live web-application
that shows the current state of the simulation in a UI.

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

## Car Washing Line

### Problem statement and simulation model

No discrete-event simulation tutorial would be considered comprehensive without the classic example of a car washing line. Here's the
scenario:

Imagine a scenario where cars arrive at a car wash in an unpredictable pattern from a finite source. At the facility, there's a single
washing line that takes approximately $d \in \mathbb{N}$ minutes to complete a cycle for each car.

Once a car finishes its wash, the next car in line is permitted to enter the washing process.

A naive approach to model this in a flow-chart could look like this:

```mermaid
---
title: Here needs a basic flowChart
---

graph LR;
    A[Start] --> B{Car Arrives};
    B -- Yes --> C(Washing Position Empty?);
    C -- Yes --> D[Start Wash];
    C -- No --> E[Put Car in Waiting Line];
    D --> F{Next Car Waiting?};
    F -- Yes --> G[Car Arrives];
    F -- No --> H[End];
    E --> B;
    G --> B;
    H --> I[End Wash];
    I --> J{Waiting Line Not Empty?};
    J -- Yes --> K[Take Car From Waiting Line];
    J -- No --> L[End];
    K --> B;

```

### Implementation of Drops-Components

In Drops we call everything that can be registered a **Component**. This is a pure function, a class-instance, a module, a
generator-function or a closure.

#### Entities and value-objects

During our implementation we will be as explicit as possible and use type annotations, aka. Annotated type-hints from the `typing.py`
module.
The first and last entity we are going to model, is the _car_.

```python title="car.py"
{!../docs_src/car_wash/001.py!}
```

As we can see, our car only has two immutable attributes, namely an Id that will serve as a plain counter and a percentage value _dirt_ that
tells us how dirty the car is.

#### Sources

Now we need something that can send a car in a specific time period to our washing line. We will call this thing a **source**.
In our case, we will model our source as a finite source sending cars every 5 minutes to our washing line.

```python title="source.py"
{!../docs_src/car_wash/002.py!}
```

Most developers would have started using a class-based approach to model our source. But since Drops is capable of registering we decide on
using
a one to model our car-source. This will make our code more concise and remove some unnecessary boilerplate as well.

First we initialize the outer function `finite_car_source_maker` with a maximum number of cars we want to send to the washing line. Then
we instantiate an infinite counter from the `itertools` module. After that we define the actual `car_source`.
In this function the counter from the outer-namespace serves as the Id for the car we want to send to the washing line and
as a counter in the while-loop. There we loop as long as we have not send enough cars which is $n_{cars} - n_{send} > 0$.

The return-type of our source is an instance of `DelayedEvent`. Drops will use this entity to create a concrete `Event` instance
in its mechanics that will be dispatched to every **Component** in the next iteration of the dispatching-algorithm.

#### Classes

The next **Component** we are going to model is the actual `WashingLine` aka. the star of our application.

```python title="washing_line.py"
{!../docs_src/car_wash/003.py!}
```