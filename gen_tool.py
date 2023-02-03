import numpy as np

path = 'elem_wise_cvt.cpp'
case_num = 10
case_num = case_num + 1
f = open(path, 'w')
str1 = '''#include "elem_wise_cvt.h"
namespace CytnxConverter {\n'''
f.write(str1)
for i in range(1, case_num):
    str1 = 'void ElemCvt_' + str(i) + '(cvt_case, itensor::ITensor& itensor_T, cytnx::UniTensor& cytnx_T);\n'
    f.write(str1)
str1 = '''void ElemWiseITensorToCytnx(const itensor::ITensor& itensor_T,
           cytnx::UniTensor* cytnx_T) {
  auto inds = itensor::inds(itensor_T);
  auto bd_num = inds.size();
  switch (bd_num) {
'''
f.write(str1)
for i in range(0, case_num):
    str1='    case ' + str(i) + ':\n'
    if i != 0:
        str1 = str1 + '       ElemCvt_' + str(i) + '(cvt_case::to_cytnx,\n'
        str1 = str1 + '                 const_cast<itensor::ITensor&>(itensor_T), *cytnx_T);\n'
    str1 = str1 + '      break;\n'
    f.write(str1)
str1 = '''    default:
      assert(false);
'''
f.write(str1)
f.write('  }\n')
f.write('}\n\n')
str1 = '''void ElemWiseCytnxToITensor(const cytnx::UniTensor& cytnx_T,
           itensor::ITensor* itensor_T) {
  auto bd_num = cytnx_T.bonds().size();
  switch (bd_num) {
'''
f.write(str1)
for i in range(0, case_num):
    str1='    case ' + str(i) + ':\n'
    if i != 0:
        str1 = str1 + '       ElemCvt_' + str(i) + '(cvt_case::to_itensor,\n'
        str1 = str1 + '                 *itensor_T, const_cast<cytnx::UniTensor&>(cytnx_T));\n'
    str1 = str1 + '      break;\n'
    f.write(str1)
str1 = '''    default:
      assert(false);
'''
f.write(str1)
f.write('  }\n')
f.write('}\n\n')

for i in range(1, case_num):
    str1 = 'void ElemCvt_' + str(i) + '(cvt_case cvt_case, itensor::ITensor& itensor_T, cytnx::UniTensor& cytnx_T) {\n'
    f.write(str1)
    str1 = '  auto inds = itensor::inds(itensor_T);\n'
    f.write(str1)
    str2 = ''
    str3 = ''
    for j in range(1, i + 1):
        str1 = '  for(long i' + str(j) + ' = 0; i' + str(j) + '< itensor::dim(inds[' + str(j - 1) + ']); ++i' + str(j) + ')\n'
        f.write(str1)
        str2 = str2 + 'i' + str(j)
        str3 = str3 + 'i' + str(j) + ' + 1'
        if j != i:
            str2 = str2 + ', '
            str3 = str3 + ', '
    str1 = '    if (cytnx_T.at({' + str2 + '}).exists()) {'
    f.write(str1 + '\n')
    str1 = '      switch (cvt_case) {\n        case cvt_case::to_cytnx: \n'
    f.write(str1)
    str1 = '          if (isReal(itensor_T)) {\n'
    f.write(str1)
    str1 = '            cytnx_T.at({' + str2 + '}) = elt(itensor_T, ' + str3 + ');\n          }'
    f.write(str1)
    str1 = ' else if (isComplex(itensor_T)) {\n'
    f.write(str1)
    str1 = '            cytnx_T.at({' + str2 + '}) = eltC(itensor_T, ' + str3 + ');\n          }'
    f.write(str1)
    str1 = ' else {assert(false);}\n'
    f.write(str1)
    str1 = '        case cvt_case::to_itensor: \n'
    f.write(str1)
    str1 = '          switch (cytnx_T.dtype()) {\n            case cytnx::Type.Double: {\n'
    str1 = str1 + '              auto val_r = cytnx_T.at<cytnx::cytnx_double>({' + str2 + '});\n'
    str1 = str1 + '              itensor_T.set(' + str3 + ', val_r);\n              break;\n            }\n'
    f.write(str1)
    str1 = '            case cytnx::Type.ComplexDouble: {\n'
    str1 = str1 + '              auto val_c = cytnx_T.at<cytnx::cytnx_complex128>({' + str2 + '});\n'
    str1 = str1 + '              itensor_T.set(' + str3 + ', val_c);\n              break;\n            }\n          }'
    f.write(str1 + '\n      }\n    }\n')
    f.write('}\n')
f.write('}\n')


f.close()
