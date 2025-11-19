From Wikipedia, the free encyclopedia
Ability of a digital electronic system to remain in unstable equilibrium forever
Figure 1. An illustration of metastability in a synchronizer, where data crosses between clock domains. In the worst case, depending on timing, the metastable condition at Ds can propagate to Dout and through the following logic into more of the system, causing undefined and inconsistent behavior.
In electronics, metastability is the ability of a digital electronic system to persist for an unbounded time in an unstable equilibrium or metastable state.[1]
In digital logic circuits, a digital signal is required to be within certain voltage or current limits to represent a '0' or '1' logic level for correct circuit operation; if the signal is within a forbidden intermediate range it may cause faulty behavior in logic gates the signal is applied to.
In metastable states, the circuit may be unable to settle into a stable '0' or '1' logic level within the time required for proper circuit operation.
As a result, the circuit can act in unpredictable ways, and may lead to a system failure, sometimes referred to as a "glitch".[2] Metastability is an instance of the Buridan's ass paradox.
Metastable states are inherent features of asynchronous digital systems, and of systems with more than one independent clock domain.
In self-timed asynchronous systems, arbiters are designed to allow the system to proceed only after the metastability has resolved, so the metastability is a normal condition, not an error condition.[3]
In synchronous systems with asynchronous inputs, synchronizers are designed to make the probability of a synchronization failure acceptably small.[4]
Metastable states are avoidable in fully synchronous systems when the input setup and hold time requirements on flip-flops are satisfied.
Retrieved from "https://en.wikipedia.org/w/index.php?title=Metastability_(electronics)&oldid=1307995581"
Categories: Electrical engineeringDigital electronicsHidden categories: Articles with short descriptionShort description is different from WikidataUse dmy dates from May 2019