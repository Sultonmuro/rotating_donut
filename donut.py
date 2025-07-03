import math,time,os


try:
    terminal_size = os.get_terminal_size()
    SCREEN_WIDTH = terminal_size.columns
    SCREEN_HEIGHT = terminal_size.lines
    print(f"Detected terminal size: {SCREEN_WIDTH} columns, {SCREEN_HEIGHT}")
except OSError:
    print("Could not detect terminal size. Falling back to default 80x24")
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT= 24
R1 =1.0
R2 =2.0


A_SPEED = 0.07 # rotation around the x-axis
B_SPEED = 0.03#rotation around the Y-axis

SHADE_CHARS = "67-,@~!#$%^&"
A=1.0
B=1.0

def clear_screen():
    if os.name == "nt":
        _ = os.system('cls')


def main():
    global A,B

    while True:
        screen_buffer = [[' '  for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
        z_buffer = [[0.0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT) ]
        for phi in range(0,628,12):
            phi /=100.0
            for theta in range(0,628,5):
                theta /=100.0


                circ_x = R2 + R1 * math.cos(theta)
                x = circ_x * math.cos(phi)
                y = circ_x * math.sin(phi)
                z = R1 * math.sin(theta)


                rotated_x_y = y * math.cos(A) - z * math.sin(A)
                rotated_x_z = y * math.sin(A) + z * math.cos(A)
                rotated_x_x = x

                final_x = rotated_x_x * math.cos(B) - rotated_x_y * math.sin(B)
                final_y = rotated_x_x * math.sin(B) + rotated_x_y * math.cos(B)
                final_z = rotated_x_z

                K2 = 5.0  # scaling factor for perspective
                ooz = 1 / (final_z + K2)

                K1 = SCREEN_WIDTH * K2 * 3/(8 * (R1 + R2))
                projected_x = int(SCREEN_WIDTH / 2 + K1 * ooz * final_x)
                projected_y = int(SCREEN_HEIGHT/2 + K1 * ooz * final_y)

                Nx = math.cos(theta) * math.cos(phi)
                Ny = math.cos(theta) * math.sin(phi)
                Nz = math.cos(theta)

                rotated_normal_y = Ny * math.cos(A) - Nz * math.sin(A)
                rotated_normal_z = Nz * math.sin(A) + Nz * math.cos(A)
                rotated_normal_x = Nx

                final_normal_x = rotated_normal_x * math.cos(B) - rotated_normal_y * math.sin(B)
                final_normal_y = rotated_normal_x * math.sin(B) + rotated_normal_y * math.cos(B)
                final_normal_z = rotated_normal_z

                L = final_normal_x * (1/math.sqrt(2)) + final_normal_y * (1/math.sqrt(2))



                #map light intensity to a shade character
                char_index = int(L * (len(SHADE_CHARS)- 1)/2 + (len(SHADE_CHARS) - 1)/2 )
                char_index = max(0,min(char_index, len(SHADE_CHARS)- 1))
                shade_char = SHADE_CHARS[char_index]


                if 0<= projected_x < SCREEN_WIDTH and 0 <= projected_y < SCREEN_HEIGHT:
                    if ooz > z_buffer[projected_y][projected_x]:
                        z_buffer[projected_y][projected_x] = ooz
                        screen_buffer[projected_y][projected_x] = shade_char
        clear_screen()

        for row in screen_buffer:
            print("".join(row))

        A+= A_SPEED
        B+=B_SPEED

        time.sleep(0.05)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #Handle Ctrl+C to exit.
        print("\nDonut stopped. GoodBye!")