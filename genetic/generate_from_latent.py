import os
import re
import time
from typing import List

import dnnlib
import numpy as np
import PIL.Image
import torch

import legacy


def load_network(network_pkl):
    print('Loading networks from "%s"...' % network_pkl)
    device = torch.device('cuda')
    with dnnlib.util.open_url(network_pkl) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device) # type: ignore
        return G

def create_random_vector(G):
    return np.random.RandomState().randn(1, G.z_dim)

def generate_image(G, latent_vector):
    device = torch.device('cuda')
    # os.makedirs(outdir, exist_ok=True)
    label = torch.zeros([1, G.c_dim], device=device)

    z = torch.from_numpy(np.array(latent_vector)).to(device)
    img = G(z, label, truncation_psi=1, noise_mode='const')
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    # filename = f'{outdir}/{str(time.time())}.png'
    return PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB') # .save(filename)
