import numpy as np
import cv2
import imageio

def get_sad(block1, block2):
    return np.sum(np.abs(block1 - block2))

def hexagonal_search(reference, current, block_size, search_area):
    hexagonal_search_points = [
        (0, -2), (-2, 0), (0, 2), (2, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)
    ]
    height, width = reference.shape
    motion_vectors = []

    for i in range(0, height - block_size + 1, block_size):
        motion_vectors_row = []
        for j in range(0, width - block_size + 1, block_size):
            min_sad = float('inf')
            mv = (0, 0)
            search_center = (i, j)

            while True:
                new_search_center = search_center
                for dx, dy in hexagonal_search_points:
                    x, y = search_center[0] + dx, search_center[1] + dy
                    if (x < 0 or y < 0 or x + block_size >= height or
                            y + block_size >= width):
                        continue
                    ref_block = reference[x:x+block_size, y:y+block_size]
                    cur_block = current[i:i+block_size, j:j+block_size]
                    sad = get_sad(ref_block, cur_block)
                    if sad < min_sad:
                        min_sad = sad
                        mv = (x - i, y - j)

                if new_search_center == search_center:
                    break

                search_center = new_search_center
                if search_center == (i, j):
                    break

            motion_vectors_row.append(mv)
        motion_vectors.append(motion_vectors_row)
    return motion_vectors
def full_search(reference, current, block_size, search_area):
    height, width = reference.shape
    motion_vectors = []

    for i in range(0, height - block_size + 1, block_size):
        motion_vectors_row = []
        for j in range(0, width - block_size + 1, block_size):
            min_sad = float('inf')
            mv = (0, 0)
            for x in range(max(0, i - search_area),
                           min(height - block_size, i + search_area)):
                for y in range(max(0, j - search_area),
                               min(width - block_size, j + search_area)):
                    ref_block = reference[x:x+block_size, y:y+block_size]
                    cur_block = current[i:i+block_size, j:j+block_size]
                    sad = get_sad(ref_block, cur_block)
                    if sad < min_sad:
                        min_sad = sad
                        mv = (x - i, y - j)
            motion_vectors_row.append(mv)
        motion_vectors.append(motion_vectors_row)
    return motion_vectors

def block_matching(reference, current, block_size=16, search_area=7,
                   search_method='hexsb'):
    # Convert images to YCbCr color space and extract Y channel
    reference_y = cv2.cvtColor(reference, cv2.COLOR_BGR2YCrCb)[:, :, 0]
    current_y = cv2.cvtColor(current, cv2.COLOR_BGR2YCrCb)[:, :, 0]
    if search_method == 'hexsb':
        motion_vectors = hexagonal_search(reference_y, current_y, block_size,
                                          search_area)
    elif search_method == 'full_search':
        motion_vectors = full_search(reference_y, current_y, block_size,
                                     search_area)
    else:
        raise ValueError("Invalid search method. Choose 'hexsb' or 'full_search'.")

    return motion_vectors


def read_yuv420_frame(file, width, height, frame_no):
    file.seek(width * height * 3 // 2 * frame_no)
    y = np.fromfile(file, dtype=np.uint8, count=width * height).reshape(height, width)
    u = np.fromfile(file, dtype=np.uint8, count=(width // 2) * (height // 2)).reshape(height // 2, width // 2)
    v = np.fromfile(file, dtype=np.uint8, count=(width // 2) * (height // 2)).reshape(height // 2, width // 2)
    return y, u, v


def convert_yuv_to_bgr(y, u, v, width, height):
    yuv = cv2.merge([y, cv2.resize(u, (width, height), interpolation=cv2.INTER_LINEAR),
                     cv2.resize(v, (width, height), interpolation=cv2.INTER_LINEAR)])
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    return bgr

def apply_motion_vectors(reference_y, motion_vectors, block_size):
    height, width = reference_y.shape
    estimated_y = np.zeros_like(reference_y)
    for i, row in enumerate(range(0, height - block_size + 1, block_size)):
        for j, col in enumerate(range(0, width - block_size + 1, block_size)):
            dx, dy = motion_vectors[i][j]
            estimated_y[row:row+block_size, col:col+block_size] = \
                reference_y[row+dx:row+block_size+dx, col+dy:col+block_size+dy]
    return estimated_y

def draw_motion_vectors(image, motion_vectors, block_size):
    img = image.copy()
    for i, row in enumerate(range(0, img.shape[0] - block_size + 1, block_size)):
        for j, col in enumerate(range(0, img.shape[1] - block_size + 1, block_size)):
            dx, dy = motion_vectors[i][j]
            start_point = (col + block_size // 2, row + block_size // 2)
            end_point = (col + block_size // 2 + dy, row + block_size // 2 + dx)
            cv2.arrowedLine(img, start_point, end_point, (0, 255, 0), 2)
    return img

## C.
def psnr(img1, img2):
    mse = np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)
    if mse == 0:
        return 100
    max_pixel_value = 255.0
    return 20 * np.log10(max_pixel_value / np.sqrt(mse))


def main():
    input_file = "paris_cif.yuv"
    width = 352
    height = 288

    with open(input_file, "rb") as file:
        frame_no = 0
        prev_frame = None
        while True:
            try:
                y, u, v = read_yuv420_frame(file, width, height, frame_no)
                if y.size == 0 or u.size == 0 or v.size == 0:
                    break

                frame = convert_yuv_to_bgr(y, u, v, width, height)

                if prev_frame is not None:
                    diff = np.sum(np.abs(frame.astype(np.int16) - prev_frame.astype(np.int16)))
                    if diff > 1000000:  # Adjust this threshold to select frames with desired differences
                        cv2.imwrite(f"frame_{frame_no - 1}.png", prev_frame)
                        cv2.imwrite(f"frame_{frame_no}.png", frame)
                        break
                prev_frame = frame
                frame_no += 1
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    """
    
    This program first defines functions for Hexagonal Search Block and Full Search block matching methods. Then, a `block_matching` function is defined, which takes as input the reference and current images, block size, search area, and search method. It converts the input images to the YCbCr color space and extracts the Y channel (brightness). Depending on the chosen search method, it calls either the `hexagonal_search` or `full_search` function to compute the motion vectors.
    
    Finally, in the `__main__` block, the program reads in the reference and current images and computes the motion vectors using both Hexagonal Search Block and Full Search block matching methods. The motion vectors are then printed to the console.
    
    Make sure to replace "reference_image.png" and "current_image.png" with the actual file paths to your reference and current
    """
    main()
    reference_img = cv2.imread("frame_0.png")
    current_img = cv2.imread("frame_1.png")
    # Hexagonal search block matching
    hexsb_motion_vectors = block_matching(reference_img, current_img,
                                          block_size=16, search_area=7,
                                          search_method='hexsb')
    print("Hexagonal Search Block matching motion vectors:")
    for row in hexsb_motion_vectors:
        print(row)

    # Full search block matching
    full_search_motion_vectors = block_matching(reference_img, current_img,
                                                block_size=16, search_area=7,
                                                search_method='full_search')
    print("Full Search Block matching motion vectors:")
    for row in full_search_motion_vectors:
        print(row)

    reference_y = cv2.cvtColor(reference_img, cv2.COLOR_BGR2YCrCb)[:, :, 0]
    current_y = cv2.cvtColor(current_img, cv2.COLOR_BGR2YCrCb)[:, :, 0]

    # Save diagrams as images
    cv2.imwrite("diagram_1.png", current_img)
    cv2.imwrite("diagram_2.png", reference_img)
    cv2.imwrite("diagram_3.png", cv2.absdiff(current_img, reference_img))

    motion_vectors_img = draw_motion_vectors(current_img, hexsb_motion_vectors, 16)
    cv2.imwrite("diagram_4.png", motion_vectors_img)

    estimated_y = apply_motion_vectors(reference_y, hexsb_motion_vectors, 16)
    estimated_img = cv2.cvtColor(np.stack([estimated_y, cv2.split(current_img)[1], cv2.split(current_img)[2]], axis=-1),
                                 cv2.COLOR_YCrCb2BGR)
    cv2.imwrite("diagram_5.png", estimated_img)

    cv2.imwrite("diagram_6.png", cv2.absdiff(estimated_img, current_img))

    ##C.
    psnr_2_1 = psnr(reference_img, current_img)
    psnr_2_5 = psnr(estimated_img, current_img)

    print("PSNR between Image 2 and Image 1:", psnr_2_1)
    print("PSNR between Image 1 and Image 5:", psnr_2_5)

    # Compute PSNR for full search
    full_search_motion_vectors = block_matching(reference_img, current_img,
                                                block_size=16, search_area=7,
                                                search_method='full_search')
    estimated_y_full = apply_motion_vectors(reference_y, full_search_motion_vectors, 16)
    estimated_img_full = cv2.cvtColor(
        np.stack([estimated_y_full, cv2.split(current_img)[1], cv2.split(current_img)[2]], axis=-1),
        cv2.COLOR_YCrCb2BGR)
    psnr_2_5_full = psnr(estimated_img_full, current_img)

    print("PSNR between Image 2 and Image 5 (Full Search):", psnr_2_5_full)

    ##D.
    print(10*"*","   D   ",10*"*")
    # Hexagonal search block matching with 8x8 blocks
    hexsb_motion_vectors_8x8 = block_matching(reference_img, current_img,
                                              block_size=8, search_area=7,
                                              search_method='hexsb')
    print("Hexagonal Search Block matching motion vectors (8x8):")
    for row in hexsb_motion_vectors_8x8:
        print(row)

    # Full search block matching with 8x8 blocks
    full_search_motion_vectors_8x8 = block_matching(reference_img, current_img,
                                                    block_size=8, search_area=7,
                                                    search_method='full_search')
    print("Full Search Block matching motion vectors (8x8):")
    for row in full_search_motion_vectors_8x8:
        print(row)

    reference_y = cv2.cvtColor(reference_img, cv2.COLOR_BGR2YCrCb)[:, :, 0]
    current_y = cv2.cvtColor(current_img, cv2.COLOR_BGR2YCrCb)[:, :, 0]

    # Save diagrams as images for 8x8 block size
    cv2.imwrite("diagram_1D.png", current_img)
    cv2.imwrite("diagram_2D.png", reference_img)
    cv2.imwrite("diagram_3D.png", cv2.absdiff(current_img, reference_img))

    motion_vectors_img_8x8 = draw_motion_vectors(current_img, hexsb_motion_vectors_8x8, 8)  # Use 8x8 motion vectors
    cv2.imwrite("diagram_4D.png", motion_vectors_img_8x8)

    estimated_y_8x8 = apply_motion_vectors(reference_y, hexsb_motion_vectors_8x8, 8)  # Use 8x8 motion vectors
    estimated_img_8x8 = cv2.cvtColor(
        np.stack([estimated_y_8x8, cv2.split(current_img)[1], cv2.split(current_img)[2]], axis=-1),
        cv2.COLOR_YCrCb2BGR)
    cv2.imwrite("diagram_5D.png", estimated_img_8x8)

    cv2.imwrite("diagram_6D.png", cv2.absdiff(estimated_img_8x8, current_img))  # Use 8x8 estimated image

    # Compute PSNR for 8x8 hexagonal search
    estimated_y_8x8 = apply_motion_vectors(reference_y, hexsb_motion_vectors_8x8, 8)
    estimated_img_8x8 = cv2.cvtColor(
        np.stack([estimated_y_8x8, cv2.split(current_img)[1], cv2.split(current_img)[2]], axis=-1), cv2.COLOR_YCrCb2BGR)
    psnr_2_5_8x8 = psnr(estimated_img_8x8, current_img)

    print("PSNR between Image 2 and Image 5 (8x8 Hexagonal Search):", psnr_2_5_8x8)

    # Compute PSNR for 8x8 full search
    estimated_y_full_8x8 = apply_motion_vectors(reference_y, full_search_motion_vectors_8x8, 8)
    estimated_img_full_8x8 = cv2.cvtColor(
        np.stack([estimated_y_full_8x8, cv2.split(current_img)[1], cv2.split(current_img)[2]], axis=-1),
        cv2.COLOR_YCrCb2BGR)
    psnr_2_5_full_8x8 = psnr(estimated_img_full_8x8, current_img)

    print("PSNR between Image 2 and Image 5 (8x8 Full Search):", psnr_2_5_full_8x8)

