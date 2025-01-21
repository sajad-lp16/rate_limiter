# RateLimiter

### Author: Sajad Tohidi Majd

Data flow is depicted in `DataflowUML.pdf` file.<br>
Screenshots are also included in `screenshots` directory (mind their names).<br>
The Code has __docs__. <br/>
no library installation is required, (requirements.txt is ignored)
no git repo :)


### Classes:
* BaseProvider:
  - 1 ) abstract provider
* Provider
  - 1 ) simulates the provider we should create on startup.
  - 2 ) in the time of instantiation it triggers a task which toggles provider and worker state.
* ProviderWorker
  - 1 ) used to respect SRP and do whatever the provider should.
  - 2 ) the validation is done again here (in case of initiated manually).
  - 3 ) manages the requests queue and inserts the request immediately (the max queue size is respected to avoid memory leaks)
  - 4 ) the provider is responsible for it active state (as the provider switched off, it will stop it worker too).
  - 5 ) when it gets a task from the queue and the provider turns off, the queue **won't** be missed and it re-queues it back.
  - 6 ) **Respects** 
    - Request execution time.
    - Request priority.
* Request
  * 1 ) a dataclass used to simulate user request.
  * 2 ) priority filed is used in `PriorityQueue` and used to compare Request objects.
* Header
  * 1 ) a hashable dict used to map headers to their validator.
* RequestController
  * 1 ) the core of rate limiter.
  * 2 ) the worker always asks `RequestsController` for permission to continue.
  * 3 ) if the Provider limit is reached it also tells the worker how much it should wait :))
* Router
  * 1 ) Maps the Provider route to Provider instance.
  * 2 ) request generator first generates the `Request` instance dynamically and routes it using Router.

DataValidation is **strict** and everywhere.<br/>
This project Uses <u>**1**</u> process and <u>**1**</u> Thread and functions concurrently using builtin **asyncio**.