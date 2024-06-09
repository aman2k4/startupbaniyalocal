from manim import *
config.media_embed = True

# // %%manim -v WARNING -s -r 160,90 --disable_caching Example

# setup manim  con
class AddLetterByLetter(Scene):
    def construct(self):
        text = Text("I will tell you what our goal is. Our goal is to make the best personal computer that we are proud to sell our family and friends.")
        self.play(AddTextLetterByLetter(text))
        self.wait()
        self.remove(text)


# add word by word animation
class AddWordByWord(Scene):
    def construct(self):
        text = Text("I will tell you what our goal is. Our goal is to make the best personal computer that we are proud to sell our family and friends.")
        self.play(AddTextWordByWord(text))
        self.wait()


if __name__ == "__main__":
    
    # run this file to create a video
    scene = AddLetterByLetter()
    scene.render()

