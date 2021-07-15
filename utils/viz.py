from torchvision.transforms.functional import to_pil_image
from torchcam.cams import SmoothGradCAMpp
from torchcam.utils import overlay_mask
from torchsummary import summary
import matplotlib.pyplot as plt

def show_model_summary(model, input_size=(3, 28, 28)):
    summary(model, input_size=input_size)


def visualize_gradcam(raw_image, processed_img, model):
    cam_extractor = SmoothGradCAMpp(model.eval())
    out = model(processed_img.unsqueeze(0))
    activation_map = cam_extractor(out.squeeze(0).argmax().item(), out)
    result = overlay_mask(
        to_pil_image(raw_image), 
        to_pil_image(activation_map, mode='F'), 
        alpha=0.5
    )
    
    plt.subplot(131)
    plt.imshow(raw_image.permute(1, 2, 0).cpu())
    plt.subplot(132)
    plt.imshow(activation_map.cpu().numpy()); plt.axis('off'); plt.tight_layout()
    plt.subplot(133)
    plt.imshow(result); plt.axis('off'); plt.tight_layout()
    plt.show()
