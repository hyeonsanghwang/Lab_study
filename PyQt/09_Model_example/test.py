import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.datasets as dsets
import torchvision.transforms as transforms


# GPU 자원 사용확인
devices_id = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.cuda.set_device(
    devices_id
)  # fix bug for `ERROR: all tensors must be on devices[0]`


# Step 1. Load Dataset
train_dataset = dsets.MNIST(root="../mnist_data", train=True, transform=transforms.ToTensor(), download=False)
test_dataset = dsets.MNIST(root="../mnist_data", train=False, transform=transforms.ToTensor(), download=False)

# Step 2. Make Dataset Iterable
batch_size = 100
train_loader = torch.utils.data.DataLoader(
    dataset=train_dataset, batch_size=batch_size, shuffle=True
)
test_loader = torch.utils.data.DataLoader(
    dataset=test_dataset, batch_size=batch_size, shuffle=False
)


# Step 3. Create Model Class
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.mp = nn.MaxPool2d(2)
        self.fc = nn.Linear(320, 10)

    def forward(self, x):
        in_size = x.size(0)
        x = F.relu(self.mp(self.conv1(x)))
        x = F.relu(self.mp(self.conv2(x)))
        x = x.view(in_size, -1)  # flatten the tensor
        outputs = self.fc(x)
        return outputs


epochs = 30
lr_rate = 0.01

# Step 4. Instantiate Model Class
model = CNN()
if devices_id == type([]):  # -> GPU
    model = nn.DataParallel(model, device_ids=devices_id).cuda()
else:
    model = nn.DataParallel(model, device_ids=[devices_id]).cuda()

# Step 5. Instantiate Loss Class
criterion = torch.nn.CrossEntropyLoss()  # computes softmax and then the cross entropy
# Step 6. Instantiate Optimizer Class
optimizer = torch.optim.SGD(model.parameters(), lr=lr_rate)


# Step 7. Train Model

# 임의의 학습 이미지를 가져옵니다
dataiter = iter(train_loader)
images, _ = dataiter.next()

loss = 0
total_iter = 0

for epoch in range(int(epochs)):
    iter = 0
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(devices_id)
        labels = labels.to(devices_id)
        optimizer.zero_grad()
        outputs = model(images)
        # Calc loss
        loss = criterion(outputs, labels)
        # Back-propagation
        loss.backward()
        # Updating wegihts
        optimizer.step()

        total_iter += 1

        iter += 1
        if iter % 200 == 0:
            # calculate Accuracy
            correct = 0
            total = 0
            for images, labels in test_loader:
                images = images.to(devices_id)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                # for gpu, bring the predicted and labels back to cpu fro python operations to work
                predicted = predicted.cpu()
                correct += (predicted == labels).sum()
            accuracy = 100 * correct / total
            print(
                f"[Epoch {epoch}] [Iteration: {i}/{len(train_loader)}] [Loss: {loss.item():.3f}] [Accuracy: {accuracy:.2f}]"
            )
