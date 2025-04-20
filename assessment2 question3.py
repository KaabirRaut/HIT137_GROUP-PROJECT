
import turtle

def draw_tree(branch_length, t, left_angle, right_angle, reduction_factor, depth):
    if depth == 0:
        return

    # Draw the main branch
    t.forward(branch_length)

    # Save current position and heading
    current_position = t.position()
    current_heading = t.heading()

    # Draw left branch
    t.left(left_angle)
    draw_tree(branch_length * reduction_factor, t, left_angle, right_angle, reduction_factor, depth - 1)

    # Return to original position and heading
    t.setposition(current_position)
    t.setheading(current_heading)

    # Draw right branch
    t.right(right_angle)
    draw_tree(branch_length * reduction_factor, t, left_angle, right_angle, reduction_factor, depth - 1)

    # Return to original position and heading
    t.setposition(current_position)
    t.setheading(current_heading)

def main():
    # User input
    left_angle = float(input("Enter left branch angle (e.g., 20): "))
    right_angle = float(input("Enter right branch angle (e.g., 25): "))
    start_length = float(input("Enter starting branch length (e.g., 100): "))
    reduction_factor = float(input("Enter branch length reduction factor (e.g., 0.7): "))
    depth = int(input("Enter recursion depth (e.g., 5): "))

    # Setup window and turtle
    window = turtle.Screen()
    window.title("Recursive Tree")

    t = turtle.Turtle()
    t.left(90)  # Point upward
    t.color("green")
    t.pensize(2)
    t.speed(0)
    t.up()
    t.goto(0, -250)
    t.down()

    draw_tree(start_length, t, left_angle, right_angle, reduction_factor, depth)

    window.mainloop()

if __name__ == "__main__":
    main()
