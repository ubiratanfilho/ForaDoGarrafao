library(OpenImageR)

files = dir("plots/", full.names = TRUE)

for (path in files){
        image = readImage(path)
        resiz = resizeImage(image, width = 1080, height = 1080, method = "nearest")
        writeImage(resiz, path)
}