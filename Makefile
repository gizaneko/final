CXX ?= g++
TARGET = a.out
TARGET2 = b.out
OBJS = colordetect.o
OBJS2 = coursedetect.o

CXXFLAGS += -c -Wall $(shell pkg-config --cflags opencv)
LDFLAGS += $(shell pkg-config --libs --static opencv)

all: $(TARGET)

$(TARGET): $(OBJS) 
	$(CXX) $< -o $@ $(LDFLAGS)

$(TARGET2): $(OBJS2) 
	$(CXX) $< -o $@ $(LDFLAGS)

%.o: %.cpp; $(CXX) $< -o $@ $(CXXFLAGS)

clean: ; rm -f $(OBJS) $(OBJS2) $(TARGET) $(TARGET2)
