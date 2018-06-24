import os
import argparse
from collections import defaultdict
import numpy as np

from mask_generator import MaskGenerator


def _parse_args():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('--quickdraw-simplified-path', default='./quickdraw_simplified', type=str, help='Path to Quickdraw simplified dataset')
    parser.add_argument('--qd-imd-path', default='./qd_imd', type=str, help='Path to newly generated QD-IMD')
    
    parser.add_argument('--shape', nargs=2, default=[512, 512], type=int, help='Output shape of masks (e.g. 512 512)')

    parser.add_argument('--n-train-masks', default=50000, type=int, help='Number of train masks to generate')
    parser.add_argument('--n-test-masks', default=10000, type=int, help='Number of test masks to generate')

    parser.add_argument('--n-drawings-per-file', default=1000, type=int, help='Number of drawings to take from every Quickdraw file')
    parser.add_argument('--n-strokes-per-drawing', default=1, type=int, help='Number of strokes to take from every drawing')

    parser.add_argument('--max-upscale-rate', default=1.5, type=float, help='Maximal scale rate of mask before central crop')

    parser.add_argument('--n-strokes-mean', default=4, type=int, help='Mean number of strokes in mask')
    parser.add_argument('--n-strokes-std', default=2, type=int, help='Std of number of strokes in mask')

    parser.add_argument('--min-stroke-width', default=5, type=float, help='Minimal width of stroke (px)')
    parser.add_argument('--max-stroke-width', default=15, type=float, help='Maximal width of stroke (px)')

    return parser.parse_args()


def main():
    np.random.seed(0)  # for reproducibility

    args = _parse_args()

    # load quickdraw drawings' paths
    all_drawing_paths = [
        os.path.join(args.quickdraw_simplified_path, name)
        for name in sorted(os.listdir(args.quickdraw_simplified_path))
    ]
    np.random.shuffle(all_drawing_paths)

    train_drawing_paths = all_drawing_paths[:len(all_drawing_paths) // 2]
    test_drawing_paths = all_drawing_paths[len(all_drawing_paths) // 2:]

    # generate QD-IMD
    if not os.path.exists(args.qd_imd_path):
        os.mkdir(args.qd_imd_path)

    hole_to_image_ratio_stats = defaultdict(list)
    for name, drawing_paths, n_masks in [('train', train_drawing_paths, args.n_train_masks),
                                        ('test', test_drawing_paths, args.n_test_masks)]:
        print('Generating {} dataset.'.format(name))
        
        dir_path = os.path.join(args.qd_imd_path, name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            
        print('It will be saved here: {}.'.format(dir_path))
        
        mask_generator = MaskGenerator(
            drawing_paths,
            shape=args.shape,
            n_drawings_per_file=args.n_drawings_per_file,
            n_strokes_per_drawing=args.n_strokes_per_drawing,
            max_upscale_rate=args.max_upscale_rate,
            n_strokes_mean=args.n_strokes_mean,
            n_strokes_std=args.n_strokes_std,
            min_stroke_width=args.min_stroke_width,
            max_stroke_width=args.max_stroke_width
        )
        
        n_saved_masks = 0
        while n_saved_masks != n_masks:
            mask = mask_generator.generate_mask()
            
            mask_np = np.array(mask)
            hole_to_image_ratio = np.sum(mask_np == False) / np.prod(mask_np.shape)
            if hole_to_image_ratio == 0:
                continue
            
            path = os.path.join(dir_path, '{:05}_{}.png'.format(n_saved_masks, name))
            mask.save(path)

            # collect stats
            hole_to_image_ratio_stats[name].append(hole_to_image_ratio)
            
            n_saved_masks += 1
            
            if n_saved_masks % 100 == 0:
                print('{:.1f}% done'.format(n_saved_masks / n_masks * 100))
        
        print()

    print('Done!')

if __name__ == '__main__':
    main()
