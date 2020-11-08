import axios from '@/libs/api.request';
/**
 * @description 获取所有标记点
 */
export const mapPointGet = (sendPage) => {
    return axios.request({
        url: 'linSystem/mapPoint/get',
        method: 'post',
        data:{
            sendPage:sendPage
        }

    })
};


/**
 * @description 搜索所有标记点
 */
export const mapPointSearch = ({sendPage,searchValue}) => {
    return axios.request({
        url: 'linSystem/mapPoint/search',
        method: 'post',
        data:{
            sendPage:sendPage,
            searchValue:searchValue
        }

    })
};

/**
 * @description 增加标记点
 */
export const addPointInfo = ({
                             mapPointName,
                             mapPointJ,
                             mapPointW,
                             mapPointAddr,
                             mapPointTel,
                             mapPointBedNum,
                             mapPointFee,
                             mapPointJian,
                             mapPointServer
                          }) => {
    return axios.request({
        url: 'linSystem/mapPointInfo/add',
        data: {
            mapPointName: mapPointName,
            mapPointJ: mapPointJ,
            mapPointW: mapPointW,
            mapPointAddr:mapPointAddr,
            mapPointTel:mapPointTel,
            mapPointBedNum:Number(mapPointBedNum),
            mapPointFee:Number(mapPointFee),
            mapPointJian:mapPointJian,
            mapPointServer:mapPointServer
        },
        method: 'post'
    })
};


/**
 * @description 上传图片
 */
export const addMapImage = (
    formData
) => {
    return axios.request({
        url: 'linSystem/mapPoint/add',
        data: formData,

        method: 'post'
        // file:file
    })
};

/**
 * @description 标记点图片点赞
 */
export const mapPointImageZan = (id) => {
    return axios.request({
        url: 'linSystem/mapPoint/imageZan',
        method: 'post',
        data:{
            mapPointId:id
        }

    })
};

/**
 * @description 标记点浏览量
 */
export const mapPointView = (id) => {
    return axios.request({
        url: 'linSystem/mapPoint/view',
        method: 'post',
        data:{
            mapPointId:id
        }

    })
};

/**
 * @description 上传视频
 */
export const addMapVedio = (
    formData
) => {
    return axios.request({
        url: 'linSystem/mapPoint/vedioAdd',
        data: formData,

        method: 'post'
        // file:file
    })
};






