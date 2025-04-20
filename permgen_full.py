#!/usr/bin/env python3

import argparse
import itertools
import string
import os
import sys
import json
import csv
import zipfile
from multiprocessing import cpu_count, Pool
from functools import partial
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Constants
SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
ZIP_THRESHOLD = 10000
EXPORT_FORMATS = ['txt', 'csv', 'json']

def get_replacements(char, mode):
    if char.isalpha() and mode['characters']:
        return [char.lower(), char.upper()]
    elif char.isdigit() and mode['digits']:
        return list(string.digits)
    elif char in SPECIAL_CHARS and mode['special']:
        return list(SPECIAL_CHARS)
    else:
        return [char]

def estimate_count(input_str, mode):
    count = 1
    variants = []
    for c in input_str:
        opts = len(get_replacements(c, mode))
        variants.append(opts)
        count *= opts
    return count, variants

def human_readable_size(bytes_):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_ < 1024:
            return f"{bytes_:.2f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.2f} PB"

def generate_chunks(input_str, mode, chunk_size=100000):
    options = [get_replacements(c, mode) for c in input_str]
    pool = itertools.product(*options)
    while True:
        chunk = list(itertools.islice(pool, chunk_size))
        if not chunk:
            break
        yield chunk

def write_to_file(filename, permutations, fmt):
    if fmt == 'txt':
        with open(filename, 'w', encoding='utf-8') as f:
            for p in permutations:
                f.write(''.join(p) + '\n')
    elif fmt == 'csv':
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for p in permutations:
                writer.writerow([''.join(p)])
    elif fmt == 'json':
        data = [''.join(p) for p in permutations]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

def compress_output(path):
    zip_path = path + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(path, arcname=os.path.basename(path))
    os.remove(path)
    return zip_path

def worker_write(chunk, fmt):
    return [''.join(p) for p in chunk] if fmt == 'json' else chunk

def save_permutations_parallel(input_str, mode, fmt='txt', max_count=None, show_progress=False):
    total, _ = estimate_count(input_str, mode)
    if max_count:
        total = min(total, max_count)

    filename = f"{input_str}.{fmt}"
    output_path = os.path.join(os.getcwd(), filename)
    data = []
    written = 0

    with Pool(cpu_count()) as pool:
        for chunk in generate_chunks(input_str, mode):
            if max_count and written >= max_count:
                break
            chunk = chunk[:max_count - written] if max_count else chunk
            processed = pool.apply(worker_write, args=(chunk, fmt))
            if fmt == 'json':
                data.extend(processed)
            else:
                write_to_file(output_path, processed, fmt)
            written += len(processed)
            if show_progress:
                print(f"Written: {written}", end='\r')

    if fmt == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    if written >= ZIP_THRESHOLD:
        zip_path = compress_output(output_path)
        return zip_path, written
    return output_path, written

# -------- GUI --------
def run_gui():
    def start():
        input_str = entry_input.get().strip()
        if not input_str:
            messagebox.showerror("Error", "Please enter a string.")
            return

        mode = {
            'characters': var_chars.get(),
            'digits': var_digits.get(),
            'special': var_special.get()
        }

        fmt = combo_format.get().lower()
        max_perms = entry_max.get().strip()
        max_perms = int(max_perms) if max_perms else None

        est, variants = estimate_count(input_str, mode)
        if max_perms:
            est = min(est, max_perms)
        size_est = human_readable_size(est * (len(input_str) + 1))

        proceed = messagebox.askyesno("Estimate", f"Estimated permutations: {est:,}\nEstimated file size: {size_est}\nContinue?")
        if not proceed:
            return

        try:
            path, total = save_permutations_parallel(input_str, mode, fmt=fmt, max_count=max_perms, show_progress=var_progress.get())
            messagebox.showinfo("Done", f"Permutations saved to:\n{path}\nTotal written: {total:,}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Permutation Generator")

    tk.Label(root, text="Input String:").grid(row=0, column=0, sticky="e")
    entry_input = tk.Entry(root, width=30)
    entry_input.grid(row=0, column=1, columnspan=2)

    var_chars = tk.BooleanVar(value=True)
    var_digits = tk.BooleanVar(value=True)
    var_special = tk.BooleanVar(value=True)
    var_progress = tk.BooleanVar(value=False)

    tk.Checkbutton(root, text="Letters", variable=var_chars).grid(row=1, column=0)
    tk.Checkbutton(root, text="Digits", variable=var_digits).grid(row=1, column=1)
    tk.Checkbutton(root, text="Specials", variable=var_special).grid(row=1, column=2)
    tk.Checkbutton(root, text="Show Progress", variable=var_progress).grid(row=2, column=0, columnspan=2)

    tk.Label(root, text="Max permutations (optional):").grid(row=3, column=0, sticky="e")
    entry_max = tk.Entry(root, width=15)
    entry_max.grid(row=3, column=1)

    tk.Label(root, text="Export Format:").grid(row=4, column=0, sticky="e")
    combo_format = ttk.Combobox(root, values=EXPORT_FORMATS, state="readonly")
    combo_format.set("txt")
    combo_format.grid(row=4, column=1)

    tk.Button(root, text="Generate", command=start).grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()

# -------- CLI --------
def main():
    parser = argparse.ArgumentParser(description="Permutation Generator CLI")
    parser.add_argument("input_string", nargs="?", help="The string to permute.")
    parser.add_argument("--characters", action="store_true", help="Include letter case variants")
    parser.add_argument("--digits", action="store_true", help="Include digit variants")
    parser.add_argument("--special", action="store_true", help="Include special character variants")
    parser.add_argument("--export", choices=EXPORT_FORMATS, default="txt", help="Export format")
    parser.add_argument("--max", type=int, help="Maximum number of permutations")
    parser.add_argument("--progress", action="store_true", help="Show progress")
    parser.add_argument("--gui", action="store_true", help="Launch GUI")
    args = parser.parse_args()

    if args.gui or not args.input_string:
        run_gui()
        return

    mode = {
        'characters': args.characters or not any([args.characters, args.digits, args.special]),
        'digits': args.digits or not any([args.characters, args.digits, args.special]),
        'special': args.special or not any([args.characters, args.digits, args.special])
    }

    est, variants = estimate_count(args.input_string, mode)
    est = min(est, args.max) if args.max else est
    size_est = human_readable_size(est * (len(args.input_string) + 1))

    print(f"Estimated permutations: {est:,}")
    print(f"Estimated file size: {size_est}")
    proceed = input("Continue? [y/N]: ").lower().strip()
    if proceed != 'y':
        print("Cancelled.")
        return

    path, total = save_permutations_parallel(
        args.input_string,
        mode,
        fmt=args.export,
        max_count=args.max,
        show_progress=args.progress
    )
    print(f"Done. Saved {total:,} permutations to {path}")

if __name__ == "__main__":
    main()
