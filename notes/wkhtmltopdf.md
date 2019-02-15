# running wkhtmltopdf on lambda

As it's know, packing pip libraries and native libraries are different, and wkhtmltopdf is a native library. Installing it on aws lambda has a specific set of things that needs to be done.

## Compiling binaries

The binaries for wkhtmltopdf has to be compiled in the same enviournement as a lambda instance. Lambda gets booted up using Aws Linux.

We can either boot up an EC2 running AmazonLinux or use docker.

### Docker

After installing docker in your system, download and boot up amazon linux

```
$ sudo docker run -it amazonlinux bash
```

### Getting the libraries

After successfully logging into the amazonlinux container, you have to install few tools first which will aid to download and unpack the dependencies.

```
# yum install -y yum-utils rpmdevtools wget
```

Now download the CentOs version of wkhtmltopdf in the container using wget into the /tmp directory.

```
# cd /tmp/
# wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox-0.12.5-1.centos6.x86_64.rpm
```

Once we have the wkhtmltopdf rpm, we'll need rpms of all of it's dependencies which we'll get using yumdownloader

```
# yum install --downloadonly --downloaddir=.  wkhtmltox-0.12.5-1.centos6.x86_64.rpm
```

We also have to get rpm of the openssl library, since it's already installed we'll use the reinstall flag

```
# yum reinstall --downloadonly --downloaddir=. openssl openssl-libs
```

Once we do it, our /tmp directory now has a bunch of rpm files which we now need to pack.

## Packing 

To pack, we must first extract all the rpms in order to get their .so files.

```
# rpmdev-extract *rpm
```

Now we'll copy all the .so files into /var/task

```
# cp /tmp/*/usr/lib64/* /var/task
```

And now we zip.

```
# zip -r9 /tmp/lib.zip *
```

## Creating Layer 

Now we need to create a layer, the structure of which should look something like

```
.
├── lib
│   ├── libcrypto.so.10
│   ├── libcrypto.so.1.0.2k
│   ├── libfontconfig.so.1
│   ├── libfontconfig.so.1.7.0
│   ├── libfontenc.so.1
│   ├── libfontenc.so.1.0.0
│   ├── libfreetype.so.6
│   ├── libfreetype.so.6.10.0
│   ├── libjpeg.so.62
│   ├── libjpeg.so.62.1.0
│   ├── libpng15.so.15
│   ├── libpng15.so.15.13.0
│   ├── libssl.so.10
│   ├── libssl.so.1.0.2k
│   ├── libX11.so.6
│   ├── libX11.so.6.3.0
│   ├── libX11-xcb.so.1
│   ├── libX11-xcb.so.1.0.0
│   ├── libXau.so.6
│   ├── libXau.so.6.0.0
│   ├── libxcb-composite.so.0
│   ├── libxcb-composite.so.0.0.0
│   ├── libxcb-damage.so.0
│   ├── libxcb-damage.so.0.0.0
│   ├── libxcb-dpms.so.0
│   ├── libxcb-dpms.so.0.0.0
│   ├── libxcb-dri2.so.0
│   ├── libxcb-dri2.so.0.0.0
│   ├── libxcb-dri3.so.0
│   ├── libxcb-dri3.so.0.0.0
│   ├── libxcb-glx.so.0
│   ├── libxcb-glx.so.0.0.0
│   ├── libxcb-present.so.0
│   ├── libxcb-present.so.0.0.0
│   ├── libxcb-randr.so.0
│   ├── libxcb-randr.so.0.1.0
│   ├── libxcb-record.so.0
│   ├── libxcb-record.so.0.0.0
│   ├── libxcb-render.so.0
│   ├── libxcb-render.so.0.0.0
│   ├── libxcb-res.so.0
│   ├── libxcb-res.so.0.0.0
│   ├── libxcb-screensaver.so.0
│   ├── libxcb-screensaver.so.0.0.0
│   ├── libxcb-shape.so.0
│   ├── libxcb-shape.so.0.0.0
│   ├── libxcb-shm.so.0
│   ├── libxcb-shm.so.0.0.0
│   ├── libxcb.so.1
│   ├── libxcb.so.1.1.0
│   ├── libxcb-sync.so.1
│   ├── libxcb-sync.so.1.0.0
│   ├── libxcb-xevie.so.0
│   ├── libxcb-xevie.so.0.0.0
│   ├── libxcb-xf86dri.so.0
│   ├── libxcb-xf86dri.so.0.0.0
│   ├── libxcb-xfixes.so.0
│   ├── libxcb-xfixes.so.0.0.0
│   ├── libxcb-xinerama.so.0
│   ├── libxcb-xinerama.so.0.0.0
│   ├── libxcb-xinput.so.0
│   ├── libxcb-xinput.so.0.1.0
│   ├── libxcb-xkb.so.1
│   ├── libxcb-xkb.so.1.0.0
│   ├── libxcb-xselinux.so.0
│   ├── libxcb-xselinux.so.0.0.0
│   ├── libxcb-xtest.so.0
│   ├── libxcb-xtest.so.0.0.0
│   ├── libxcb-xvmc.so.0
│   ├── libxcb-xvmc.so.0.0.0
│   ├── libxcb-xv.so.0
│   ├── libxcb-xv.so.0.0.0
│   ├── libXext.so.6
│   ├── libXext.so.6.4.0
│   ├── libXfont.so.1
│   ├── libXfont.so.1.4.1
│   ├── libXrender.so.1
│   ├── libXrender.so.1.3.0
│   ├── libzip.so.5
│   └── libzip.so.5.0.0
└── wkhtmltopdf
```

## Running on Lambda

After you've set up the layer and attached it to your lambda function. The first issue you're gonna run into is: 

```
wkhtmltopdf exited with non-zero code 1. error:\n/opt/wkhtmltopdf: /lib64/libcrypto.so.10: version `OPENSSL_1.0.2' not found (required by /opt/wkhtmltopdf)
```

The issue that's happening here is that, AmazonLinux has switched to using openssl 1.0.2 however lambda builds are still stuck with 1.0.1, and because we compiled the binaries in an amazonlinux instance they're looking for openssl 1.0.2.

We've already attached openssl 1.0.2 in our libs but lambda doesn't seem to recognize it.

Now, linux looks for library files in folders listed in an enviourment variable called LD_LIBRARY_PATH, the default value of which is: 

<pre>
/lib64:/usr/lib64:$LAMBDA_RUNTIME_DIR:$LAMBDA_RUNTIME_DIR/lib:$LAMBDA_TASK_ROOT:$LAMBDA_TASK_ROOT/lib:<b>/opt/lib</b>
</pre>

As you can see, /opt/lib where our layer is mounted is the last parameter, so naturally lambda looks for ssh in /lib64 first, where it finds it, but gets the wrong version of it. 

We can fix this by overriding the enviourment variable and setting /opt/lib as the first priority.

<pre>
<b>/opt/lib</b>:/lib64:/usr/lib64:$LAMBDA_RUNTIME_DIR:$LAMBDA_RUNTIME_DIR/lib:$LAMBDA_TASK_ROOT:$LAMBDA_TASK_ROOT/lib
</pre>

Once we do this, everything should work properly.