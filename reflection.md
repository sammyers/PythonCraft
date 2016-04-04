### Technical Review - Reflection and Synthesis

In our review, we asked for people's ideas about how we should order the application of algorithms to generate the terrain, how we might efficiently store and load data for our generated worlds, how to design the architecture of the program, and any additional features that might be interesting.

We allocated the first third of our time block to explain the project and summarize our current progress, and the remaining time to discuss design and implementation choices. For the most part, the time was utilized as we intended; we spent an appropriate amount of time on explanations and, although it was less sequentially organized for different topics than we planned, the remaining time consisted of useful discussion and questions.

Considering the somewhat esoteric nature of the topics involved in this project, like OpenGL rendering, we tried to remain conscious about not going into too much detail. We think we did a reasonable job keeping the discussion within a helpful scope.

It was suggested that we generate the terrain in two phases in order to make cave systems and other three-dimensional features underneath the surface, by first creating a first-pass heightmap and then overlaying Perlin Noise or some other algorithm to 'carve' features into the existing terrain. It was also suggested that we include recognizable landmarks, which would be interesting but possibly contradictory to the spirit of the project.

Paul suggested that we look into using octrees for more efficient data loading and storage, so that we don't have to store map data in full resolution for areas that aren't visible. We've done some research and will probably try a basic implementation, but I (Sam) am skeptical about the speed of accessing or modifying entries in this kind of data structure (having to traverse through some number of nodes) as opposed to using chunking with traditional arrays.

We didn't get to ask for recommendations about program structure, but this was one of our lesser concerns. 

At this stage in the project we were mostly trying to implement the basic features that we had already figured out, so we didn't have a lot of questions for our audience to help with. In a future technical review, we intend to devote more effort to thinking of discussion questions that will produce constructive feedback.